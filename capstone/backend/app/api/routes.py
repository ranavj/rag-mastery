"""
API route handlers — /api/health, /api/upload, /api/chat.  (Day 20+)

Schemas: app.models.schemas (Pydantic = frontend types.ts ka mirror).
"""

import os

from fastapi import APIRouter, File, Form, UploadFile

from app.config import UPLOAD_DIR
from app.ingestion.pipeline import ingest_pdf
from app.models.schemas import HealthResponse, UploadResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/upload", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    company_id: str = Form(...),
) -> UploadResponse:
    """PDF upload -> disk pe save -> ingest (chunk+embed+Chroma) -> {doc_id, chunks}."""
    try:
        dest = os.path.join(UPLOAD_DIR, f"{company_id}__{file.filename}")
        with open(dest, "wb") as f:
            f.write(await file.read())

        doc_id, chunks = ingest_pdf(dest, company_id=company_id)
        return UploadResponse(doc_id=doc_id, chunks=chunks, status="ok")
    except Exception:
        return UploadResponse(doc_id="", chunks=0, status="error")


# Day 21-22: POST /chat -> retrieval+generation, phir agent
