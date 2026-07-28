"""
Retrieval: Chroma search (company_id filter) + threshold.  (Day 21)

REUSE: Day 7 (top_k + distance threshold — kam=better). company_id `where` filter
       = per-tenant isolation (Day 5). NAYA kuch nahi, bas API ke andar.
(Rerank Day 15 = optional, eval se prove — abhi nahi.)
"""

from app.ingestion.pipeline import get_collection

# Probe se tuned (Day 21): in-corpus ~0.42-0.56, out-of-corpus ~0.81+ → 0.7 beech me.
DISTANCE_THRESHOLD = 0.7
TOP_K = 4


def retrieve(question: str, company_id: str, k: int = TOP_K) -> list[dict]:
    """
    Tenant ke docs me search → threshold paar karne wale chunks.
    returns [{text, page, doc_id, distance}, ...]  (khaali = kuch relevant nahi mila).
    """
    col = get_collection()
    res = col.query(
        query_texts=[question],
        n_results=k,
        where={"company_id": company_id},   # per-tenant isolation
    )

    hits = []
    for text, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        if dist <= DISTANCE_THRESHOLD:        # Day 7: kam distance = zyada relevant
            hits.append(
                {
                    "text": text,
                    "page": meta.get("page"),
                    "doc_id": meta.get("doc_id"),
                    "distance": dist,
                }
            )
    return hits
