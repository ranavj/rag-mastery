"""
Day 8 — RAGBot: sab skills ek reusable ENGINE mein (Phase 2 capstone)
=====================================================================
6 din ki skills ek class mein:
  ingest() = load(D6) → clean(D6) → chunk(D3) → store(D5)   [ek baar]
  ask()    = tuned-retrieve(D7) → Claude(D1) → answer + citations(D6)  [har sawaal]

Frontend analogy: ek ApiClient service class — ek baar bana lo, kahin bhi use karo
(CLI, Streamlit, React). Engine UI se ALAG (separation of concerns).
"""

import os
import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
BASE = os.path.dirname(__file__)

# tuning knobs (Day 7) — ek jagah, easily badalne layak
CHUNK_SIZE, CHUNK_OVERLAP = 500, 80
TOP_K = 4
DISTANCE_THRESHOLD = 1.4          # isse door = reject (anti-hallucination)


class RAGBot:
    def __init__(self, collection_name="ragbot"):
        self.client = chromadb.PersistentClient(path=os.path.join(BASE, "chroma_db"))
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.llm = Anthropic()

    # ---------- INGEST: pipeline (ek baar) ----------
    def ingest(self, pdf_path: str) -> int:
        if self.collection.count() > 0:
            return self.collection.count()      # already ingested (persist!)

        docs = PyPDFLoader(pdf_path).load()                 # D6 load
        for d in docs:                                      # D6 clean
            d.page_content = self._clean(d.page_content, d.metadata["page"] + 1)

        splitter = RecursiveCharacterTextSplitter(          # D3 chunk
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        chunks = splitter.split_documents(docs)

        self.collection.add(                                # D5 store
            ids=[f"c{i}" for i in range(len(chunks))],
            documents=[c.page_content for c in chunks],
            metadatas=[{"source": os.path.basename(c.metadata["source"]),
                        "page": c.metadata["page"] + 1} for c in chunks],
        )
        return len(chunks)

    @staticmethod
    def _clean(text: str, page_num: int) -> str:
        for junk in ["BAJAJ FINANCE LIMITED",
                     "Internal Policy Reference Document — CONFIDENTIAL",
                     "For internal use only | Bajaj Finance Limited | FY 2024-25 | "
                     "Unauthorised distribution prohibited", f"Page {page_num}"]:
            text = text.replace(junk, "")
        return "\n".join(ln.strip() for ln in text.split("\n") if ln.strip())

    # ---------- ASK: retrieve → generate (har sawaal) ----------
    def ask(self, query: str) -> dict:
        res = self.collection.query(query_texts=[query], n_results=TOP_K)

        # D7 threshold — door wale reject
        good = [(d, m) for d, dist, m in zip(
                    res["documents"][0], res["distances"][0], res["metadatas"][0])
                if dist <= DISTANCE_THRESHOLD]

        if not good:
            return {"answer": "Mujhe iski jaankari policy mein nahi mili. "
                              "Kripya customer support se sampark karein.",
                    "sources": []}

        context = "\n\n".join(f"[page {m['page']}] {d}" for d, m in good)
        prompt = (f"Tum Bajaj Finance ke helpdesk assistant ho. SIRF neeche diye "
                  f"CONTEXT se jawab do. Na ho to bolo 'jaankari nahi hai'.\n\n"
                  f"CONTEXT:\n{context}\n\nSAWAAL: {query}\n\nJAWAB (short, Hinglish):")

        resp = self.llm.messages.create(
            model="claude-sonnet-4-6", max_tokens=400,
            messages=[{"role": "user", "content": prompt}])

        pages = sorted({m["page"] for _, m in good})
        return {"answer": resp.content[0].text, "sources": pages}


# ---------- CLI test (terminal chat) ----------
if __name__ == "__main__":
    bot = RAGBot()
    n = bot.ingest(os.path.join(BASE, "sample_docs", "bajaj_finance_policy_reference.pdf"))
    print(f"🤖 RAGBot ready ({n} chunks). 'quit' se bahar.\n")

    while True:
        q = input("👤 Aap: ").strip()
        if q.lower() in {"quit", "exit", ""}:
            break
        out = bot.ask(q)
        print(f"\n🤖 Bot: {out['answer']}")
        if out["sources"]:
            print(f"   📄 Source: policy.pdf, page(s) {out['sources']}\n")
        else:
            print()
