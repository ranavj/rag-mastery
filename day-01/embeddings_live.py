"""
Day 1 (bonus) — Embeddings ko AANKHON se dekho
===============================================
Yeh script asli numbers dikhata hai:
  - ek sentence ka vector kaisa dikhta hai (numbers ki list)
  - kaunse sentences ek doosre ke "paas" hain (cosine similarity score)

Free local model use kar rahe (all-MiniLM-L6-v2) — koi API key nahi, offline.
"""

from sentence_transformers import SentenceTransformer, util

# Model load — yeh wahi "embed()" function hai. Text do, vector lo.
# (pehli baar download hota hai, phir cache se instant)
print("Model load ho raha hai...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Humara chhota knowledge base (jaise Day 1 mein tha)
documents = [
    "Refund policy: 30 din ke andar paisa wapas milta hai.",   # money/refund
    "Shipping standard delivery 5-7 din leti hai.",            # shipping
    "Payment ke liye UPI aur card accept karte hain.",         # payment
]

# User ka sawaal — note: ismein "refund" shabd hai hi nahi! "paise" bola hai.
query = "Mujhe mera paise wapas kab milenge?"

# STEP 1: sab ko vectors mein badlo (embed karo)
doc_vectors = model.encode(documents)
query_vector = model.encode(query)

# Ek vector kaisa dikhta hai? Pehle 8 numbers dekho (poora 384 lamba hai!)
print(f"\nVector ki lambai (dimensions): {len(query_vector)}")
print(f"Query vector ke pehle 8 numbers: {query_vector[:8].round(3)}")

# STEP 2: query har doc se kitna similar hai? (cosine similarity, 0 se 1)
print(f"\n👤 Query: {query}\n")
print("Similarity scores (zyada = zyada relevant):")
scores = util.cos_sim(query_vector, doc_vectors)[0]
for doc, score in zip(documents, scores):
    bar = "█" * int(score * 20)   # chhota visual bar
    print(f"  {score:.3f} {bar:20s} | {doc}")

# Sabse zyada score wala = jeet gaya = yahi retrieve hoga
best = documents[scores.argmax()]
print(f"\n✅ Sabse relevant: {best}")
print("\n👀 Notice: query mein 'refund' shabd nahi tha, phir bhi refund wala doc jeeta!")
print("   Kyunki embedding ne MEANING pakda, shabd nahi. Yahi hai magic.")
