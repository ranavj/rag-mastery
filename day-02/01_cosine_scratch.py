"""
Day 2 — File 1: Cosine Similarity FROM SCRATCH (pure Python math)
=================================================================
Kal humne library se score dekha. Aaj woh number KHUD banayenge,
sirf jodna-guna-squareroot se. Har line ke aage comment mein VALUE likhi hai
taaki padhte waqt dikhe ki andar kya number ban raha hai.

Mithai example: Gulab Jamun=[10,0], Rasgulla=[9,0]   ([meetha, teekha])
"""

import math
from sentence_transformers import SentenceTransformer, util


# ===================================================================
# FUNCTION 1: dot_product — "jodi-jodi guna karke jodo"
# ===================================================================
def dot_product(a, b):
    total = 0
    for ai, bi in zip(a, b):     # zip = a aur b ko saath chalao:
        #                          chakkar 1: ai=10, bi=9
        #                          chakkar 2: ai=0,  bi=0
        total += ai * bi         # chakkar 1: total = 0 + (10*9) = 90
        #                          chakkar 2: total = 90 + (0*0) = 90
    return total                 # <-- return: 90


# ===================================================================
# FUNCTION 2: magnitude — vector ki "size"/lambai (Pythagoras)
# ===================================================================
def magnitude(v):
    # v=[10,0] hai toh:
    #   x*x har number pe ->  10*10=100 ,  0*0=0
    #   sum(...)          ->  100 + 0 = 100
    #   math.sqrt(100)    ->  10.0
    return math.sqrt(sum(x * x for x in v))   # <-- return: 10.0 (a ke liye)


# ===================================================================
# FUNCTION 3: cosine_similarity — sab ko jodo: dot / (lenA * lenB)
# ===================================================================
def cosine_similarity(a, b):
    d = dot_product(a, b)        # d  = 90   (function 1 se)
    la = magnitude(a)            # la = 10   (function 2 se, a ke liye)
    lb = magnitude(b)            # lb = 9    (function 2 se, b ke liye)
    return d / (la * lb)         # 90 / (10*9) = 90/90 = 1.0  <-- SCORE


# ===================================================================
# PART B — chhote vectors pe test (math khud aankhon se verify karo)
# ===================================================================
print("=== Test 1: simple vectors ===")

gulab  = [10, 0]   # bahut meetha, koi teekha nahi
rasgul = [9, 0]    # bahut meetha, koi teekha nahi  -> similar
samosa = [0, 8]    # koi meetha nahi, teekha        -> alag

print(f"GulabJamun vs Rasgulla = {cosine_similarity(gulab, rasgul):.3f}  (expect ~1.0, similar)")
print(f"GulabJamun vs Samosa   = {cosine_similarity(gulab, samosa):.3f}  (expect 0.0, alag)")
# Samosa wale mein: dot = (10*0)+(0*8) = 0  ->  0/(...) = 0.0


# ===================================================================
# PART C — asli text embeddings pe lagao, library se MILAO
# ===================================================================
print("\n=== Test 2: asli text — humara math vs library ===")
model = SentenceTransformer("all-MiniLM-L6-v2")

text_a = "Mujhe refund chahiye"
text_b = "Mera paisa wapas karo"

vec_a = model.encode(text_a).tolist()   # 384 numbers ki list
vec_b = model.encode(text_b).tolist()   # 384 numbers ki list

mera_score    = cosine_similarity(vec_a, vec_b)                                  # humara function
library_score = util.cos_sim(model.encode(text_a), model.encode(text_b))[0][0].item()  # library

print(f"Mera scratch score : {mera_score:.4f}")
print(f"Library score      : {library_score:.4f}")
print("✅ MATCH!" if abs(mera_score - library_score) < 0.001 else "❌ mismatch")
