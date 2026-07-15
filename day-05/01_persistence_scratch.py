"""
Day 5 — File 1: PERSISTENCE from scratch (disk pe save/load)
=============================================================
Kal ka MiniVectorStore RAM mein tha -> script band = sab gayab.
Aaj usme save() + load() jodenge — khud, bina library ke.

Frontend analogy (EXACT same pattern!):
  save() = localStorage.setItem("store", JSON.stringify(data))
  load() = JSON.parse(localStorage.getItem("store"))
Bas "localStorage" ki jagah ek FILE hai disk pe.
"""

import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Path ko SCRIPT ke location se baandho (na ki jahan se chalaya) —
# warna doosre folder se chalane pe FileNotFoundError aata (relative path bug!)
# __file__ = is script ka apna path; dirname = uska folder
STORE_FILE = os.path.join(os.path.dirname(__file__), "my_store.json")


class MiniVectorStore:
    def __init__(self):
        self.docs = []
        self.vectors = []      # numpy arrays

    def add(self, texts: list[str]):
        for t in texts:
            self.docs.append(t)
            self.vectors.append(model.encode(t))
        print(f"✅ {len(texts)} docs embed+add hue. Total: {len(self.docs)}")

    def search(self, query: str, top_k: int = 2):
        q = model.encode(query)
        scores = [float(np.dot(q, v) / (np.linalg.norm(q) * np.linalg.norm(v)))
                  for v in self.vectors]
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [(self.docs[i], scores[i]) for i in ranked[:top_k]]

    # ---------- NAYA: SAVE (localStorage.setItem jaisa) ----------
    def save(self):
        data = {
            "docs": self.docs,
            # numpy array JSON mein nahi jata -> .tolist() se normal list banao
            # (bilkul JSON.stringify se pehle object ko serializable banana)
            "vectors": [v.tolist() for v in self.vectors],
        }
        with open(STORE_FILE, "w") as f:
            json.dump(data, f)              # = JSON.stringify + file write
        print(f"💾 Store disk pe saved: {STORE_FILE}")

    # ---------- NAYA: LOAD (localStorage.getItem jaisa) ----------
    def load(self) -> bool:
        if not os.path.exists(STORE_FILE):   # pehli baar? file nahi hogi
            return False
        with open(STORE_FILE) as f:
            data = json.load(f)              # = JSON.parse
        self.docs = data["docs"]
        self.vectors = [np.array(v) for v in data["vectors"]]  # list -> numpy wapas
        print(f"⚡ Disk se load hua: {len(self.docs)} docs (KOI RE-EMBEDDING NAHI!)")
        return True


# ------------------------------------------------------------------
# DEMO — magic yahan dikhega
# ------------------------------------------------------------------
if __name__ == "__main__":
    store = MiniVectorStore()

    # Pehle disk se load try karo (jaise app khulte hi localStorage check)
    if not store.load():
        print("🆕 Pehli baar — embed karke save karte hain (yeh SLOW hai)...")
        store.add([
            "Refund 30 din ke andar milta hai.",
            "Delivery 5-7 working days leti hai.",
            "Warranty 1 saal ki hoti hai.",
            "Payment UPI aur card se hota hai.",
        ])
        store.save()

    # Search hamesha kaam karega — chahe embed kiya ho ya load
    query = "Mera paisa kab wapas aayega?"
    print(f"\n👤 Query: {query}")
    for doc, score in store.search(query):
        print(f"   {score:.3f} | {doc}")

    print("\n🔁 AB YEH SCRIPT DOBARA CHALAO — dekho kya hota hai!")
