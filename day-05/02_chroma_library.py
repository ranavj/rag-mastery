"""
Day 5 — File 2: ChromaDB (asli persistent vector database)
============================================================
Humara scratch JSON store "khilona" tha. Chroma real cheez hai:
  - persist: disk pe automatic (PersistentClient) — humara save/load FREE mila
  - metadata: har doc ke saath extra info (source, category...)
  - filter:   search + WHERE ek saath (SQL ka WHERE / JS ka .filter())
  - embedding: KHUD karta hai — text do, bas! (andar default all-MiniLM hi hai 😄)

Frontend analogy: scratch = khud ka localStorage jugaad;
Chroma = IndexedDB + query engine (proper database).
"""

import os
import chromadb

# ---- STEP 1: Persistent client — folder batao, disk pe DB ban jayega ----
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")   # (path lesson applied!)
client = chromadb.PersistentClient(path=DB_DIR)

# ---- STEP 2: Collection = table (SQL) / object store (IndexedDB) ----
# get_or_create = pehli baar banao, agli baar wahi kholo (persistence!)
collection = client.get_or_create_collection(name="policies")

# ---- STEP 3: Add — sirf pehli baar (dobara run pe skip) ----
if collection.count() == 0:
    print("🆕 Pehli baar — docs add ho rahe (Chroma khud embed karega)...")
    collection.add(
        # ids: har doc ka unique naam (DB primary key jaisa) — zaroori hai
        ids=["doc1", "doc2", "doc3", "doc4", "doc5"],
        documents=[
            "Refund 30 din ke andar milta hai.",
            "Delivery standard 5-7 working days leti hai.",
            "Express delivery sirf 2 din mein ho jaati hai.",
            "Warranty har electronic product par 1 saal ki hai.",
            "Payment UPI, card aur cash on delivery se hota hai.",
        ],
        # metadata: har doc ke saath extra info — filtering ke liye
        metadatas=[
            {"category": "refund",   "source": "policy.pdf"},
            {"category": "shipping", "source": "policy.pdf"},
            {"category": "shipping", "source": "faq.md"},
            {"category": "warranty", "source": "policy.pdf"},
            {"category": "payment",  "source": "faq.md"},
        ],
    )
else:
    print(f"⚡ DB disk pe already hai — {collection.count()} docs loaded (no re-embed!)")

# ---- STEP 4: Search (Chroma query khud embed karta hai) ----
print("\n=== Search 1: normal semantic search ===")
result = collection.query(query_texts=["saamaan kitne din mein aayega?"], n_results=2)
for doc, dist, meta in zip(result["documents"][0], result["distances"][0], result["metadatas"][0]):
    print(f"   dist={dist:.3f} | {doc}  [{meta['category']}]")
# NOTE: Chroma DISTANCE deta hai (L2 jaisa) -> KAM = zyada similar (Day 4 bonus yaad hai!)

# ---- STEP 5: Search + METADATA FILTER (yeh FAISS mein NAHI tha!) ----
print("\n=== Search 2: wahi query, par sirf 'shipping' category mein ===")
result = collection.query(
    query_texts=["saamaan kitne din mein aayega?"],
    n_results=2,
    where={"category": "shipping"},        # <- SQL ka WHERE! sirf shipping docs
)
for doc, dist, meta in zip(result["documents"][0], result["distances"][0], result["metadatas"][0]):
    print(f"   dist={dist:.3f} | {doc}  [{meta['category']}]")

print("\n🔁 Script dobara chalao — '⚡ already hai' dikhega (persistence FREE mili!)")
