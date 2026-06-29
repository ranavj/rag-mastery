"""
Day 1 — RAG from scratch (zero RAG libraries)
==============================================

Frontend dev ke liye: socho yeh ek search widget ka backend hai.
- KNOWLEDGE_BASE       -> ek hardcoded "API response" / mock data array
- retrieve()           -> .filter() jaisa — query se matching items dhundo
- ask_claude()         -> render() — data ko le ke final output banao

Hum yahan jaan-bujh ke koi RAG framework (LangChain/Chroma) use NAHI kar rahe.
Sirf Python + Claude. Taaki andar ka mechanism saaf dikhe.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# .env se ANTHROPIC_API_KEY uthao (bilkul jaise Vite/Angular env vars)
load_dotenv()


# ----------------------------------------------------------------------
# STEP 1: "Knowledge Base" — yeh aapke documents hain.
# Real app mein yeh PDF/DB se aata, abhi simple list (mock data).
# Har item ek "chunk" hai — ek chhota text piece.
# ----------------------------------------------------------------------
KNOWLEDGE_BASE = [
    "Refund policy: Product delivery ke 30 din ke andar full refund milta hai, bina koi sawaal.",
    "Shipping: Standard delivery 5-7 working days leti hai. Express delivery 2 din mein.",
    "Warranty: Har electronic product par 1 saal ki manufacturer warranty hoti hai.",
    "Support: Customer care subah 9 baje se raat 9 baje tak available hai, 7 din.",
    "Payment: Hum UPI, credit/debit card, aur cash on delivery accept karte hain.",
]


# ----------------------------------------------------------------------
# STEP 2: RETRIEVE — query se relevant chunks dhundo.
# Abhi sabse simple tareeka: keyword overlap (shabd milte hain kya).
# Yeh React mein array.filter(item => item.includes(word)) jaisa hai.
#
# NOTE: Yeh "naive" search hai — sirf exact shabd match karta hai.
# Day 2 mein hum ise "semantic" banayenge (meaning se match) embeddings se.
# ----------------------------------------------------------------------
def retrieve(query: str, top_k: int = 2) -> list[str]:
    query_words = set(query.lower().split())

    scored = []
    for chunk in KNOWLEDGE_BASE:
        chunk_words = set(chunk.lower().split())
        # kitne shabd common hain = score
        overlap = len(query_words & chunk_words)
        scored.append((overlap, chunk))

    # sabse zyada matching pehle (sort + top_k uthao)
    scored.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [chunk for score, chunk in scored[:top_k] if score > 0]
    return top_chunks


# ----------------------------------------------------------------------
# STEP 3: AUGMENT + GENERATE — retrieved context + query Claude ko do.
# Yeh "render(data)" jaisa hai: data le ke final UI (answer) banao.
# ----------------------------------------------------------------------
def ask_claude(query: str, context_chunks: list[str]) -> str:
    client = Anthropic()  # key automatically .env se uthata hai

    context_text = "\n".join(f"- {c}" for c in context_chunks)

    # Yeh prompt = "props" jo hum LLM component ko pass kar rahe hain
    prompt = f"""Tum ek helpful customer support assistant ho.
Sirf neeche diye CONTEXT ke basis par jawab do. Agar context mein answer na ho, bolo "Mujhe iski jaankari nahi hai".

CONTEXT:
{context_text}

SAWAAL: {query}

JAWAB (Hindi/Hinglish mein, short):"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


# ----------------------------------------------------------------------
# MAIN — pura RAG flow ek jagah
# ----------------------------------------------------------------------
if __name__ == "__main__":
    user_query = "Mujhe refund kitne din mein milega?"

    print(f"\n👤 User: {user_query}\n")

    # 1. Retrieve
    chunks = retrieve(user_query, top_k=2)
    print("🔍 Retrieved chunks (yeh Claude ko bheje jaayenge):")
    for c in chunks:
        print(f"   • {c}")

    # 2. Augment + Generate
    print("\n🤖 Claude soch raha hai...\n")
    answer = ask_claude(user_query, chunks)
    print(f"✅ Answer: {answer}\n")
