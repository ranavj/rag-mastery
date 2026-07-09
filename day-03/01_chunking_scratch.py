"""
Day 3 — File 1: CHUNKING from scratch (pure Python)
====================================================
Bade document ko chhote overlapping tukdo (chunks) mein todna.

Core idea (jo tumne khud derive kiya):
  - har chunk  = chunk_size lamba
  - har step   = chunk_size - overlap   (itna aage badho)
  - overlap    = pichhle chunk ka thoda hissa repeat -> context bacha rahe

Frontend analogy: pagination — poora data (1 chunk) nahi, na har item alag;
page-by-page usable tukde. Overlap = git diff ke context lines.
"""


# -------------------------------------------------------------------
# CHUNKING FUNCTION — dil of Day 3
# -------------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = 30, overlap: int = 10) -> list[str]:
    chunks = []
    start = 0
    step = chunk_size - overlap          # kitna aage badhna hai har baar

    # jab tak text bacha hai, tukde kaatte jao
    while start < len(text):
        end = start + chunk_size         # is chunk ka end
        chunk = text[start:end]          # slice: start se end tak (frontend: array.slice)
        chunks.append(chunk)
        start += step                    # agle chunk ke liye 'step' aage badho

    return chunks


# -------------------------------------------------------------------
# DEMO 1 — chhote text pe, taaki overlap AANKHON se dikhe
# -------------------------------------------------------------------
print("=== Demo 1: chhota text, overlap dikhe ===")
text = "RAG ek powerful technique hai jo LLM ko fresh data deti"
print(f"Poora text ({len(text)} chars): {text}\n")

chunks = chunk_text(text, chunk_size=30, overlap=10)
for i, c in enumerate(chunks):
    print(f"Chunk {i+1} (start={i*20}): '{c}'")
# Notice: har chunk ke shuru ke ~10 char pichhle chunk ke end se match karenge = overlap


# -------------------------------------------------------------------
# DEMO 2 — overlap ka fayda: 0 overlap vs 10 overlap
# -------------------------------------------------------------------
print("\n=== Demo 2: overlap 0 vs 10 (boundary problem) ===")
policy = "Maternity leave 26 hafte ki hoti hai. Yeh leave delivery se pehle shuru hoti hai."

print("\n-- BINA overlap (overlap=0): --")
for i, c in enumerate(chunk_text(policy, chunk_size=40, overlap=0)):
    print(f"  Chunk {i+1}: '{c}'")

print("\n-- overlap=15 ke saath: --")
for i, c in enumerate(chunk_text(policy, chunk_size=40, overlap=15)):
    print(f"  Chunk {i+1}: '{c}'")
print("\n(dekho overlap wale mein context repeat hota hai -> meaning nahi tut-ti)")
