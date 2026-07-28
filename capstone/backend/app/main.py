"""
FastAPI entrypoint — SmartSupport backend.  (Day 20)

Run (capstone/backend/ se):
    uvicorn app.main:app --reload
Docs auto: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import FRONTEND_ORIGIN

app = FastAPI(title="SmartSupport")

# CORS — React (5173) se browser call allow (Day 23 ke liye ready)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
