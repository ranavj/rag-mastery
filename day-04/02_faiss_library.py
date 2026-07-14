"""
Day 4 — File 2: Vector Store with FAISS (real library)
=======================================================
Scratch store har vector se cosine nikalta tha (exhaustive).
FAISS wahi kaam INDEX bana ke fast karta hai. Interface same, andar smart.

Yahan hum FAISS ka "IndexFlatIP" use karenge:
  - IP = Inner Product (dot product)
  - agar vectors ko NORMALIZE kar do (length = 1), toh inner product = cosine similarity!
    (yaad hai cosine = dot / (magA*magB); magnitude 1 ho to bas dot bacha = cosine)

FAISS numpy float32 arrays maangta hai (yeh uska "data format" hai).
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

docs = [
    "Refund 30 din ke andar milta hai.",
    "Delivery 5-7 working days leti hai.",
    "Warranty 1 saal ki hoti hai.",
    "Payment UPI aur card se hota hai.",
]

# STEP 1: sab docs embed karo -> numpy float32 (FAISS ka format)
doc_vectors = model.encode(docs).astype("float32")

# STEP 2: NORMALIZE (length = 1) taaki inner product = cosine
faiss.normalize_L2(doc_vectors)

# STEP 3: INDEX banao — dimension batao (384), phir vectors add karo
dimension = doc_vectors.shape[1]        # 384
index = faiss.IndexFlatIP(dimension)    # IP index (cosine ke liye)
index.add(doc_vectors)                  # <- yahan FAISS "index" ban gaya
print(f"✅ FAISS index ready. Vectors stored: {index.ntotal}")

# STEP 4: SEARCH
query = "Mera paisa kab wapas aayega?"
q_vec = model.encode([query]).astype("float32")
faiss.normalize_L2(q_vec)               # query ko bhi normalize

top_k = 2
scores, indices = index.search(q_vec, top_k)
# search() 2 cheezein deta hai:
#   scores  = similarity scores (cosine, kyunki normalized)
#   indices = kaunse doc (unka position number)

print(f"\n👤 Query: {query}\n")
print("🔍 FAISS top results:")
for score, idx in zip(scores[0], indices[0]):
    print(f"   {score:.3f} | {docs[idx]}")

print("\n👀 Compare karo 01_vectorstore_scratch.py ke output se —")
print("   same docs, same order aana chahiye. FAISS = wahi kaam, bas fast + scalable.")
