"""
Day 2 — File 2: SEMANTIC RAG (cosine search + Claude)
======================================================
Day 1 ka retrieve() KEYWORD se dhundta tha (exact shabd). Aaj usko
MEANING se dhundvayenge — cosine similarity se. Phir Claude se jawab.

Flow:  query -> embed -> har doc se cosine -> top docs -> Claude -> answer
Frontend: filter(exact)  ->  sort(by score).slice(0, top_k)
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util

load_dotenv()
model = SentenceTransformer("all-MiniLM-L6-v2")


# Knowledge base — wahi Day 1 wala
KNOWLEDGE_BASE = [
    "Refund policy: Product delivery ke 30 din ke andar full refund milta hai.",
    "Shipping: Standard delivery 5-7 working days. Express 2 din.",
    "Warranty: Har electronic product par 1 saal ki warranty.",
    "Support: Customer care subah 9 se raat 9 baje tak, 7 din.",
    "Payment: UPI, credit/debit card, aur cash on delivery accept.",
]

# Saare documents ko EK BAAR embed kar lo (yeh "index" ban gaya).
# Real app mein yeh vector DB mein save hota — abhi memory mein.
DOC_VECTORS = model.encode(KNOWLEDGE_BASE)


# -------------------------------------------------------------------
# SEMANTIC RETRIEVE — Day 1 ke keyword retrieve ka upgrade
# -------------------------------------------------------------------
def retrieve(query: str, top_k: int = 2) -> list[str]:
    query_vec = model.encode(query)                 # sawaal ko vector banao

    # har doc se cosine score (ek list of scores milti hai)
    scores = util.cos_sim(query_vec, DOC_VECTORS)[0]

    # score ke hisaab se index sort karo, top_k uthao (sort + slice)
    top_indexes = scores.argsort(descending=True)[:top_k]

    return [(KNOWLEDGE_BASE[i], scores[i].item()) for i in top_indexes]


# -------------------------------------------------------------------
# GENERATE — context + query Claude ko do (Day 1 jaisa hi)
# -------------------------------------------------------------------
def ask_claude(query: str, chunks: list[str]) -> str:
    client = Anthropic()
    context = "\n".join(f"- {c}" for c in chunks)
    prompt = f"""Tum helpful support assistant ho. Sirf CONTEXT se jawab do.
Agar context mein na ho toh bolo "Mujhe iski jaankari nahi hai".

CONTEXT:
{context}

SAWAAL: {query}

JAWAB (short, Hinglish):"""
    res = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return res.content[0].text

# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
if __name__ == "__main__":
    # NOTE: query mein "refund" shabd JAAN-BUJH ke nahi daala —
    # Day 1 ka keyword search yahan FAIL hota, semantic PASS hoga.
    query = "Mera paisa kitne din mein wapas aayega?"
    print(f"\n👤 User: {query}\n")

    results = retrieve(query, top_k=2)
    print("🔍 Semantic retrieve (score ke saath):")
    for doc, score in results:
        print(f"   {score:.3f} | {doc}")

    chunks = [doc for doc, score in results]
    print("\n🤖 Claude soch raha hai...\n")
    print(f"✅ Answer: {ask_claude(query, chunks)}\n")
