"""
Retrieval: Chroma search (company_id filter) + threshold + optional rerank.

SKELETON (Day 19). Day 21 me bharega.
REUSE: Day 7 (top_k + threshold + MMR), Day 15 (CrossEncoder rerank — optional,
       eval se prove). company_id `where` filter = per-tenant isolation (Day 5).
"""

# def retrieve(question: str, company_id: str, k: int = 4) -> list[dict]:
#     """returns chunks [{text, page, doc_id}, ...] for the given tenant."""
#     ...
