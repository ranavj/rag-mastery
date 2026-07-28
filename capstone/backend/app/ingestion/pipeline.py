"""
Ingestion pipeline: upload file -> clean -> chunk -> embed -> Chroma.

SKELETON (Day 19). Day 20 me bharega.
REUSE: Day 6 (PyPDFLoader + clean), Day 3 (RecursiveCharacterTextSplitter),
       Day 5 (Chroma persistent). Metadata: company_id + source + page + doc_id.
"""

# def ingest(file_path: str, company_id: str) -> tuple[str, int]:
#     """returns (doc_id, num_chunks). Chroma me company_id metadata ke saath store."""
#     ...
