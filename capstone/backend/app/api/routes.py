"""
API route handlers — /api/upload, /api/chat, /api/health.

SKELETON (Day 19). Fills up:
  - Day 20: POST /upload  -> ingestion.pipeline
  - Day 21: POST /chat    -> retrieval + generation (plain RAG)
  - Day 22: POST /chat    -> agent ke through (tool_used add)

Schemas: app.models.schemas (UploadResponse, ChatRequest, ChatResponse, HealthResponse)
"""

# from fastapi import APIRouter, UploadFile, Form
# from app.models.schemas import ChatRequest, ChatResponse, UploadResponse, HealthResponse
#
# router = APIRouter()
#
# @router.get("/health", response_model=HealthResponse)
# def health(): ...
#
# @router.post("/upload", response_model=UploadResponse)
# async def upload(file: UploadFile, company_id: str = Form(...)): ...
#
# @router.post("/chat", response_model=ChatResponse)
# def chat(req: ChatRequest): ...
