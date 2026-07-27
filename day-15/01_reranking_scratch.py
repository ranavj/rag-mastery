"""
Day 15 — Re-ranking (2-stage retrieval) from scratch
====================================================
Problem: bi-encoder (Day 2 wala cosine) query aur doc ko ALAG-ALAG embed karta hai.
         Doc ka vector query ko "dekhe bina" (ingest time) banta hai -> match ROUGH.
         Kabhi-kabhi galat doc top pe aa jata hai.

Fix (Re-ranking): DO STAGE.
  Stage 1 (fast, rough)  : bi-encoder cosine -> thode EXTRA candidates (shortlist)
  Stage 2 (slow, sateek) : cross-encoder query+doc ko EK SAATH dekh ke score de -> dobaara sort

Cross-encoder scratch nahi ban sakta (woh trained neural model hai) — par 2-stage ka
poora LOOP haath se likhenge (library wrapper nahi). Real model use, orchestration humari.

Frontend: autocomplete (fast, kachi list)  ->  phir dhyaan se sort (accurate)
Hiring:   ATS keyword filter (500->50)      ->  interview (50->best 3)
"""

import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder

# Stage 1 model = BI-ENCODER (query & doc alag-alag -> vector). Wahi Day 2 wala.
bi_encoder = SentenceTransformer("all-MiniLM-L6-v2")

# Stage 2 model = CROSS-ENCODER (query+doc EK SAATH -> ek relevance score).
# ms-marco = search relevance pe trained. NOTE: chhota L-6 model is corpus pe FAIL
# hua tha (echo-trap ko #1 rakha) -> L-12 (bada, ~130MB) ne sahi kiya. Reranker ki
# QUALITY matter karti hai (jaise embedding model ki karti thi).
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")


# Knowledge base. Query ek KHAAS model (SonicWave) ka concrete jawab (kitne ghante)
# maangti hai. D1/D2 query ke shabd echo karte hain par jawab/model NAHI dete. D3 me
# model naam hai par battery ka jawab nahi. Sahi jawab (D0) ek LAMBE noisy paragraph
# me dabaa hai + synonyms use karta ("keeps going before plugged in") -> bi-encoder
# ka cosine patla. Cross-encoder D0 me se sahi answer-span + model match pakad ke upar laayega.
DOCS = [
    ("Founded in 2012, our audio company designs premium speakers loved by customers worldwide. From compact "
     "travel units to large home theatre systems, we focus on rich sound and long-lasting build quality. "
     "The SonicWave model keeps going for about eighteen hours before it needs to be plugged in again."),      # D0 = SAHI (jawab + model, dabaa hua)
    "The number of hours a speaker can play on one charge usually depends on the volume level you choose.",     # D1 TRAP: query shabd echo, jawab nahi
    "Details about how many hours each speaker plays on a single charge are printed on the retail box.",        # D2 TRAP: query shabd echo, jawab nahi
    "The SonicWave speaker is available in three colours and supports the latest Bluetooth 5.0 standard.",      # D3 model naam hai, par battery jawab nahi
    "Standard shipping usually takes 5 to 7 working days for most delivery locations across the country.",      # D4 off-topic
]

QUERY = "How many hours does the SonicWave speaker play on one charge?"

# saare docs EK BAAR embed (index) — query yahan maujood NAHI (isliye rough)
doc_vecs = bi_encoder.encode(DOCS)


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# -------------------------------------------------------------------
# STAGE 1 — Bi-encoder cosine se SHORTLIST (fast, rough)
# thode EXTRA candidates lo (yahan 4) — final me se zyada, taaki sahi doc
# kahin shortlist me aa hi jaaye (bhale rank 1 pe na ho).
# -------------------------------------------------------------------
def stage1_retrieve(query, shortlist_k=4):
    q_vec = bi_encoder.encode(query)
    scores = [(i, cosine(q_vec, dv)) for i, dv in enumerate(doc_vecs)]
    scores.sort(key=lambda x: x[1], reverse=True)      # sort by cosine, high->low
    return scores[:shortlist_k]                        # [(doc_index, cosine), ...]


# -------------------------------------------------------------------
# STAGE 2 — Cross-encoder RE-RANK (slow, sateek)
# har candidate ke liye [query, doc] PAIR banao -> model ek saath dekh ke score de.
# phir un scores se DOBAARA sort. (yeh loop = "re-ranking", haath se.)
# -------------------------------------------------------------------
def stage2_rerank(query, candidate_indexes, final_k=2):
    pairs = [[query, DOCS[i]] for i in candidate_indexes]   # query+doc SAATH
    ce_scores = cross_encoder.predict(pairs)                # ek score per pair
    ranked = sorted(zip(candidate_indexes, ce_scores),
                    key=lambda x: x[1], reverse=True)       # dobaara sort
    return ranked[:final_k]


if __name__ == "__main__":
    print(f"QUERY: {QUERY}\n")

    # ---- STAGE 1 output ----
    shortlist = stage1_retrieve(QUERY, shortlist_k=4)
    print("STAGE 1 — bi-encoder cosine (fast, rough):")
    for rank, (i, s) in enumerate(shortlist, 1):
        print(f"  {rank}. [D{i}] cos={s:.3f}  {DOCS[i][:60]}...")

    # ---- STAGE 2 output ----
    candidate_indexes = [i for i, _ in shortlist]
    reranked = stage2_rerank(QUERY, candidate_indexes, final_k=len(candidate_indexes))
    print("\nSTAGE 2 — cross-encoder re-rank (slow, sateek):")
    for rank, (i, s) in enumerate(reranked, 1):
        print(f"  {rank}. [D{i}] ce={s:+.3f}  {DOCS[i][:60]}...")

    print(f"\nFINAL best doc: [D{reranked[0][0]}] {DOCS[reranked[0][0]]}")
