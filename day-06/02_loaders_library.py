"""
Day 6 — File 2: LangChain Loader + FULL REAL PIPELINE
======================================================
Aaj ka climax — saari 5 din ki skills ek pipeline mein, ASLI PDF pe:

  PDF → [LOAD] → [CLEAN 🧹] → [CHUNK (Day 3)] → [CHROMA (Day 5)] → [SEARCH]

LangChain ka PyPDFLoader "Document" objects deta hai:
  doc.page_content  = text
  doc.metadata      = {"source": "...pdf", "page": 3}   <- REAL metadata!
Day 5 mein yeh label FAKE tha (humne haath se likha) — aaj SACH hai.
"""

import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE = os.path.dirname(__file__)
PDF_PATH = os.path.join(BASE, "sample_docs", "bajaj_finance_policy_reference.pdf")

# ------------------------------------------------------------------
# STEP 1: LOAD — PyPDFLoader = pypdf ka LangChain wrapper
# Har page ek "Document" object banta hai (text + metadata saath-saath)
# ------------------------------------------------------------------
loader = PyPDFLoader(PDF_PATH)
raw_docs = loader.load()
print(f"📄 Loaded: {len(raw_docs)} pages (Document objects)")
print(f"   Sample metadata: {raw_docs[2].metadata}")   # dekho — source + page REAL hai!

# ------------------------------------------------------------------
# STEP 2: CLEAN 🧹 — har page se repeated header/footer hatao
# (warna har chunk mein milawat -> blurry vectors -> kharab retrieval)
# ------------------------------------------------------------------
BOILERPLATE = [
    "BAJAJ FINANCE LIMITED",
    "Internal Policy Reference Document — CONFIDENTIAL",
    "For internal use only | Bajaj Finance Limited | FY 2024-25 | Unauthorised distribution prohibited",
]

def clean_page(text: str, page_num: int) -> str:
    for junk in BOILERPLATE:
        text = text.replace(junk, "")
    text = text.replace(f"Page {page_num}", "")   # "Page 3" jaisi lines
    # khali lines squeeze karo
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    return "\n".join(lines)

for doc in raw_docs:
    before = len(doc.page_content)
    doc.page_content = clean_page(doc.page_content, doc.metadata["page"] + 1)
    # (pypdf page 0-indexed hota metadata mein; PDF text mein 1-indexed tha)

print(f"🧹 Cleaned: boilerplate hata (page 3: {before} chars pehle)")

# ------------------------------------------------------------------
# STEP 3: CHUNK (Day 3 ki skill) — ab METADATA ke saath!
# split_documents() text todta hai PAR har chunk ko uske page ka
# metadata VIRASAT mein deta hai. (split_text sirf strings deta tha)
# ------------------------------------------------------------------
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
chunks = splitter.split_documents(raw_docs)
print(f"✂️  Chunked: {len(chunks)} chunks (size=500, overlap=80)")
print(f"   Chunk #5 ka metadata: {chunks[5].metadata}")   # page number saath aaya!

# ------------------------------------------------------------------
# STEP 4: CHROMA (Day 5 ki skill) — REAL metadata ke saath store
# ------------------------------------------------------------------
client = chromadb.PersistentClient(path=os.path.join(BASE, "chroma_db"))
collection = client.get_or_create_collection(name="bajaj_policy")

if collection.count() == 0:
    print("🆕 Chroma mein daal rahe (embed hoga, thoda time)...")
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=[c.page_content for c in chunks],
        metadatas=[{"source": os.path.basename(c.metadata["source"]),
                    "page": c.metadata["page"] + 1} for c in chunks],
    )
print(f"💾 Chroma ready: {collection.count()} chunks stored")

# ------------------------------------------------------------------
# STEP 5: SEARCH — aur ab result mein PAGE NUMBER bhi milega!
# ------------------------------------------------------------------
query = "What is the penalty for EMI bounce?"
print(f"\n👤 Query: {query}\n")
result = collection.query(query_texts=[query], n_results=3)
for doc, dist, meta in zip(result["documents"][0], result["distances"][0], result["metadatas"][0]):
    print(f"   dist={dist:.3f} | 📄 {meta['source']} — PAGE {meta['page']}")
    print(f"      \"{doc[:120].strip()}...\"\n")

print("🎯 Dekho — ab hum bata sakte hain jawab KIS PAGE se aaya. Yahi 'citations' ka base hai!")
