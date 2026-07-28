"""
Ingestion pipeline: PDF -> clean -> chunk -> embed -> Chroma.  (Day 20)

REUSE: Day 6 (PyPDFLoader + clean), Day 3 (RecursiveCharacterTextSplitter),
       Day 5 (Chroma persistent). NAYA: har chunk me company_id + doc_id metadata
       (multi-tenant isolation — retrieval `where={"company_id": ...}` se filter karega).
"""

import os
import uuid

import chromadb
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHROMA_DIR, COLLECTION, EMBED_MODEL

# ek hi embedding function (all-MiniLM-L6-v2, Day 2) — ingest + retrieval dono same use karein
_embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)


def get_collection() -> chromadb.Collection:
    """Shared Chroma collection (Day 21 retrieval bhi yahi use karega)."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(name=COLLECTION, embedding_function=_embed_fn)


def _clean(text: str) -> str:
    """Generic clean — khali lines squeeze (Day 6). Arbitrary upload, isliye light."""
    return "\n".join(ln.strip() for ln in text.split("\n") if ln.strip())


def ingest_pdf(file_path: str, company_id: str) -> tuple[str, int]:
    """
    PDF ko chunk+embed karke Chroma me daalo (company_id tag ke saath).
    returns (doc_id, num_chunks).
    """
    # 1) LOAD — har page ek Document (text + metadata) [Day 6]
    raw_docs = PyPDFLoader(file_path).load()

    # 2) CLEAN [Day 6]
    for d in raw_docs:
        d.page_content = _clean(d.page_content)

    # 3) CHUNK — metadata (source, page) virasat me [Day 3]
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_documents(raw_docs)

    # 4) STORE [Day 5] — doc_id + company_id + page metadata ke saath
    doc_id = uuid.uuid4().hex[:8]
    source = os.path.basename(file_path)
    collection = get_collection()
    collection.add(
        ids=[f"{doc_id}_{i}" for i in range(len(chunks))],
        documents=[c.page_content for c in chunks],
        metadatas=[
            {
                "company_id": company_id,
                "doc_id": doc_id,
                "source": source,
                "page": c.metadata.get("page", 0) + 1,  # pypdf 0-indexed -> human 1-indexed
            }
            for c in chunks
        ],
    )
    return doc_id, len(chunks)
