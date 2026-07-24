"""
Day 14 — HyDE (Hypothetical Document Embeddings) from scratch
=============================================================
Problem: query (chhota sawaal) aur document (bada jawab) ka ROOP alag ->
         cosine kamzor.
HyDE fix: query -> LLM se FARAZ jawab banwao (document jaisa) -> use search karo.
(Faraz jawab galat ho to bhi chalega — sirf DHUNDHNE ke liye hai, dene ke liye nahi.)

Comparison: normal retrieval (query se) vs HyDE (faraz-jawab se) — kaunsa better match?
"""

import os
import numpy as np
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
model = SentenceTransformer("all-MiniLM-L6-v2")
client = Anthropic()

# chhota knowledge base (documents = "jawab-roop", formal)
DOCS = [
    "Refund Policy: Refund is processed within 30 days of product delivery once the returned item passes quality check.",
    "Shipping Policy: Standard delivery takes 5 to 7 working days. Express delivery is completed within 2 days.",
    "Warranty Policy: Every electronic product carries a 1 year manufacturer warranty against defects.",
]
doc_vecs = model.encode(DOCS)


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def best_match(query_vec):
    scores = [cosine(query_vec, dv) for dv in doc_vecs]
    i = int(np.argmax(scores))
    return DOCS[i], scores


# ---- HyDE: query se ek faraz jawab banwao ----
def make_hypothetical_answer(query: str) -> str:
    prompt = (f"Ek customer ne poocha: '{query}'. "
              f"Ek chhota, seedha jawab likho jaise policy document me hota "
              f"(2-3 line, bhale exact number galat ho — bas policy-jaisa likho).")
    resp = client.messages.create(model="claude-sonnet-4-6", max_tokens=120,
                                  messages=[{"role": "user", "content": prompt}])
    return resp.content[0].text.strip()


if __name__ == "__main__":
    # aisi query jiska roop document se bahut alag hai (chhoti, casual)
    query = "mera paisa kab tak wapas aa jayega?"
    print(f"👤 Query: {query}\n")

    # --- Tarika A: NORMAL (query se seedha search) ---
    q_vec = model.encode(query)
    doc_a, scores_a = best_match(q_vec)
    print("=== A) NORMAL retrieval (query se) ===")
    print(f"   scores: " + ", ".join(f"{s:.2f}" for s in scores_a))
    print(f"   best: {doc_a[:55]}...\n")

    # --- Tarika B: HyDE (faraz jawab se search) ---
    hypo = make_hypothetical_answer(query)
    print("=== B) HyDE retrieval (faraz jawab se) ===")
    print(f"   🔮 faraz jawab: {hypo[:90]}...")
    h_vec = model.encode(hypo)
    doc_b, scores_b = best_match(h_vec)
    print(f"   scores: " + ", ".join(f"{s:.2f}" for s in scores_b))
    print(f"   best: {doc_b[:55]}...\n")

    print("🎯 Compare scores — HyDE me Refund doc ka score BADHA? (faraz jawab document-jaisa)")
