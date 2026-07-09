"""
Day 3 — File 2: SMART CHUNKING with LangChain
==============================================
Scratch version characters gin ke kaat-ta tha -> words tootte the (Yeh -> Ye+h).
Library "RecursiveCharacterTextSplitter" smart hai: natural boundaries pe kaat-ta hai.

Kaise? Uske paas separators ki PRIORITY LIST hai:
    ["\\n\\n", "\\n", " ", ""]
    = pehle paragraph (\\n\\n) pe todne ki koshish,
      na ho to line (\\n) pe,
      na ho to space ( ) pe  <- yahan word poora rehta hai!,
      last resort: character pe.
Isiliye "recursive" — upar se neeche try karta jata hai jab tak chunk fit na ho.

Frontend analogy: CSS `word-break` — `break-word` shabd todta hai,
par `normal` pehle space pe todne ki koshish karta hai. Yeh 'normal' jaisa hai.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


policy = "Maternity leave 26 hafte ki hoti hai. Yeh leave delivery se pehle shuru hoti hai."


# -------------------------------------------------------------------
# Library splitter banao — same size/overlap jaisa scratch mein tha
# -------------------------------------------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=40,       # ek chunk max 40 chars
    chunk_overlap=15,    # 15 char overlap (context ke liye)
    separators=["\n\n", "\n", " ", ""],   # priority: para -> line -> word -> char
)

library_chunks = splitter.split_text(policy)

print("=== LIBRARY (smart) chunking ===")
for i, c in enumerate(library_chunks):
    print(f"  Chunk {i+1} ({len(c)} chars): '{c}'")

print("\n👀 Dekho: koi shabd beech se nahi kata (space pe kaata) -> saaf chunks")
print("   Scratch mein 'Yeh' -> 'Ye'+'h' hua tha. Yahan word poore hain.")
