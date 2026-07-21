"""
Day 7 — File 2: Retrieval tuning with LangChain (library)
==========================================================
Wahi 3 knobs — ab LangChain retriever ke built-in modes se:
  - search_type="similarity_score_threshold"  (humara EXP-2 threshold)
  - search_type="mmr" (k, fetch_k, lambda_mult)  (humara EXP-3 MMR)

LangChain "as_retriever()" = vectorstore ke upar ek tuned-search remote control.
"""

import os
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Day-6 collection LangChain wrapper se kholo
# (embedding wahi all-MiniLM — jo Chroma default ne use kiya tha)
BASE = os.path.dirname(__file__)
emb = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    collection_name="bajaj_policy",
    embedding_function=emb,
    persist_directory=os.path.join(BASE, "..", "day-06", "chroma_db"),
)
print(f"💾 Vectorstore loaded via LangChain\n")

# ------------------------------------------------------------------
# MODE 1: THRESHOLD retriever — kachra reject (built-in)
# NOTE: yeh SIMILARITY score use karta (0-1, zyada=better) — distance ka ULTA!
# ------------------------------------------------------------------
threshold_retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.25},  # sim < 0.25 = reject
    # (pehle 0.3 rakha tha -> EMI query 0.297 pe THI, 0.003 se reject ho gayi thi!
    #  lesson: threshold hamesha ASLI scores dekh ke tune karo, hawa mein nahi)
)

print("=" * 60)
print("MODE 1: threshold retriever")
print("=" * 60)
for q in ["What is the penalty for EMI bounce?", "What is the price of a large pizza?"]:
    docs = threshold_retriever.invoke(q)
    if docs:
        print(f"✅ '{q[:35]}...' -> {len(docs)} docs (p{docs[0].metadata['page']} top)")
    else:
        print(f"❌ '{q[:35]}...' -> kuch nahi mila (rejected) — imaandaar!")

# ------------------------------------------------------------------
# MODE 2: MMR retriever — diversity (built-in)
# fetch_k = kitne candidates lao (bade pool se), k = final kitne chuno
# lambda_mult = humara lam (1=sirf relevance, 0=sirf diversity)
# ------------------------------------------------------------------
print("\n" + "=" * 60)
print("MODE 2: MMR retriever (k=3, fetch_k=10, lambda_mult=0.5)")
print("=" * 60)
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5},
)
for d in mmr_retriever.invoke("EMI payment rules and charges"):
    print(f"  p{d.metadata['page']} | {d.page_content[:65].strip()}...")

print("\n👀 LangChain ka MMR internally NORMALIZED similarity use karta —")
print("   isliye lambda=0.5 pe bhi kaam karta (humara scale-mismatch wala dard nahi!)")
