"""
API contract — BACKEND side (Pydantic).

Yeh file frontend ke `frontend/src/api/types.ts` ka MIRROR hai.
Dono ko hamesha match rakho = "single source of truth" discipline.
Day 19 pe finalize (Day 20-22 me routes inhe use karenge).
"""

from typing import Literal, Optional

from pydantic import BaseModel


# ---------- POST /api/upload  (multipart: file + company_id) ----------
class UploadResponse(BaseModel):
    doc_id: str
    chunks: int                       # kitne chunks bane + store hue
    status: Literal["ok", "error"]


# ---------- POST /api/chat ----------
class ChatRequest(BaseModel):
    company_id: str
    question: str


class Source(BaseModel):
    """Ek citation — kaunse doc/page se jawab aaya (Day 6 metadata)."""
    text: str
    page: Optional[int] = None
    doc_id: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source] = []                                   # RAG tool chala to citations
    tool_used: Literal["policy_search", "account_api", "none"]   # agent ne kya chuna (Day 17-18)


# ---------- GET /api/health ----------
class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
