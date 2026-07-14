"""
Day 4 — File 1: Mini Vector Store FROM SCRATCH
================================================
FAISS ka simplest version khud banate hain — taaki samajh aaye
ek "vector store" andar karta kya hai.

Ek vector store 2 kaam karta hai:
  - add()    : documents ko embed karke store karo
  - search() : query se top-k similar docs dhundo

Frontend analogy: yeh ek "service/store" class hai (jaise Angular service ya
React context) jo data hold karti hai + methods deti hai.

NOTE: hum abhi EXHAUSTIVE search kar rahe (har doc se compare) — yani "Flat" index.
Asli FAISS ismein clustering laga ke ise fast banata hai (Day ka concept).
Interface wahi rehta hai, sirf andar ka search smart hota hai.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


class MiniVectorStore:
    def __init__(self):
        self.docs = []       # original text (jaise DB ki rows)
        self.vectors = []    # unke embeddings (jaise DB ka index column)

    # ---- ADD: doc ko embed karke store karo ----
    def add(self, texts: list[str]):
        for t in texts:
            self.docs.append(t)
            self.vectors.append(model.encode(t))   # text -> vector
        print(f"✅ {len(texts)} docs added. Total store mein: {len(self.docs)}")

    # ---- cosine similarity (Day 2 wala, numpy se short) ----
    def _cosine(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        # np.dot = dot product, np.linalg.norm = magnitude — wahi Day 2 formula

    # ---- SEARCH: query se top-k similar docs ----
    def search(self, query: str, top_k: int = 2):
        q_vec = model.encode(query)

        # har stored vector se cosine (EXHAUSTIVE — yahi FAISS optimize karta)
        scores = [self._cosine(q_vec, v) for v in self.vectors]

        # score ke hisaab se index sort karke top-k
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [(self.docs[i], scores[i]) for i in ranked[:top_k]]


# ------------------------------------------------------------------
# DEMO
# ------------------------------------------------------------------
if __name__ == "__main__":
    store = MiniVectorStore()

    store.add([
        "Refund 30 din ke andar milta hai.",
        "Delivery 5-7 working days leti hai.",
        "Warranty 1 saal ki hoti hai.",
        "Payment UPI aur card se hota hai.",
    ])

    query = "Mera paisa kab wapas aayega?"
    print(f"\n👤 Query: {query}\n")

    print("🔍 Top results:")
    for doc, score in store.search(query, top_k=2):
        print(f"   {score:.3f} | {doc}")
