"""
API route handlers — /api/health, /api/upload, /api/chat.  (Day 20+)

Schemas: app.models.schemas (Pydantic = frontend types.ts ka mirror).
"""

import os

from fastapi import APIRouter, File, Form, UploadFile

from app.agent.agent import run_agent
from app.config import UPLOAD_DIR
from app.ingestion.pipeline import ingest_pdf
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    Source,
    UploadResponse,
)

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


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """
    AGENTIC (Day 22): agent KHUD tool chunta (policy_search / account_api / none).
    tool_used ab ASLI decision hai (Day 21 me hardcode tha).
    """
    text, sources, tool_used = run_agent(req.question, company_id=req.company_id)
    return ChatResponse(
        answer=text,
        sources=[Source(**s) for s in sources],
        tool_used=tool_used,
    )
