"""
Day 7 — File 1: Retrieval Quality ke 3 knobs (scratch)
=======================================================
Day 6 ka bajaj_policy collection REUSE (40 chunks, dobara embed nahi).

3 experiments:
  1. top_k     — kitne chunks? (kam=miss, zyada=noise)
  2. threshold — kachra reject ("jawab nahi mila" bolna seekho)
  3. MMR       — diversity (relevant BHI, aapas mein ALAG bhi) — formula KHUD
"""

import os
import numpy as np
import chromadb

# Day 6 ka collection kholo (path Day-6 folder ka!)
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "day-06", "chroma_db")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="bajaj_policy")
print(f"💾 Collection loaded: {collection.count()} chunks (Day 6 se reuse)\n")


# ==================================================================
# EXPERIMENT 1: top_k — same query, alag k
# ==================================================================
print("=" * 60)
print("EXP 1: top_k ka khel — 'EMI bounce penalty?'")
print("=" * 60)
query = "What is the penalty for EMI bounce?"

for k in [1, 3, 6]:
    res = collection.query(query_texts=[query], n_results=k)
    print(f"\n--- k={k} ---")
    for doc, dist, meta in zip(res["documents"][0], res["distances"][0], res["metadatas"][0]):
        print(f"  {dist:.3f} | p{meta['page']} | {doc[:60].strip()}...")
# Dekhna: k=1 risky (ek hi chance), k=6 mein neeche wale kitne door/irrelevant?


# ==================================================================
# EXPERIMENT 2: THRESHOLD — jawab docs mein HAI HI NAHI wali query
# ==================================================================
print("\n" + "=" * 60)
print("EXP 2: threshold — 'pizza ka price?' (PDF mein hai hi nahi!)")
print("=" * 60)
junk_query = "What is the price of a large pizza?"

res = collection.query(query_texts=[junk_query], n_results=3)
print("\n-- BINA threshold (Chroma phir bhi 3 'results' dega): --")
for doc, dist in zip(res["documents"][0], res["distances"][0]):
    print(f"  {dist:.3f} | {doc[:60].strip()}...")

# Ab threshold lagao — door wale reject
THRESHOLD = 1.3   # isse zyada distance = query se bahut door = kachra

def search_with_threshold(q: str, k: int = 3):
    res = collection.query(query_texts=[q], n_results=k)
    good = [(d, dist, m) for d, dist, m in
            zip(res["documents"][0], res["distances"][0], res["metadatas"][0])
            if dist <= THRESHOLD]                    # <- yahi threshold logic
    return good

print(f"\n-- Threshold={THRESHOLD} ke saath: --")
for q in [junk_query, query]:
    good = search_with_threshold(q)
    if not good:
        print(f"  '{q[:40]}...' -> ❌ Jawab nahi mila (sab reject) — SAHI behaviour!")
    else:
        print(f"  '{q[:40]}...' -> ✅ {len(good)} chunks paas hue")


# ==================================================================
# EXPERIMENT 3: MMR from scratch — greedy select (relevance + diversity)
# ==================================================================
print("\n" + "=" * 60)
print("EXP 3: MMR — 'EMI payment rules' (repeat vs variety)")
print("=" * 60)
mmr_query = "EMI payment rules and charges"

# Pehle zyada candidates lao (fetch_k=10) EMBEDDINGS ke saath
res = collection.query(query_texts=[mmr_query], n_results=10,
                       include=["documents", "distances", "metadatas", "embeddings"])
docs   = res["documents"][0]
metas  = res["metadatas"][0]
vecs   = np.array(res["embeddings"][0])
# query ka vector bhi chahiye — chroma se hi nikaal lo (1 result ka embedding trick nahi,
# simple: distance use karke relevance banayenge: relevance = -distance)
dists  = np.array(res["distances"][0])

def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def mmr_select(top_k=3, lam=0.5):
    """lam=1 -> sirf relevance (normal search); lam=0 -> sirf diversity"""
    selected = []
    candidates = list(range(len(docs)))
    while len(selected) < top_k and candidates:
        best_i, best_score = None, -1e9
        for i in candidates:
            relevance = -dists[i]                      # kam distance = zyada relevant
            # already-selected se MAX similarity (kitna repeat hoga)
            repeat = max((cosine(vecs[i], vecs[j]) for j in selected), default=0)
            score = lam * relevance - (1 - lam) * repeat   # <- MMR FORMULA
            if score > best_score:
                best_i, best_score = i, score
        selected.append(best_i)
        candidates.remove(best_i)
    return selected

print("\n-- lam=1.0 (sirf relevance = normal search): --")
for i in mmr_select(lam=1.0):
    print(f"  p{metas[i]['page']} | {docs[i][:65].strip()}...")

print("\n-- lam=0.5 (MMR: relevance + diversity balance): --")
for i in mmr_select(lam=0.5):
    print(f"  p{metas[i]['page']} | {docs[i][:65].strip()}...")

# lam=0.5 pe kuch nahi badla tha (scale mismatch!) — ab diversity ko ZYADA awaaz do:
print("\n-- lam=0.1 (diversity ki awaaz 9x zyada): --")
for i in mmr_select(lam=0.1):
    print(f"  p{metas[i]['page']} | {docs[i][:65].strip()}...")

print("\n🎯 Compare karo: ab results alag-alag PAGES/topics se aaye?")
