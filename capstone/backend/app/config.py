"""
Settings — env vars, paths, model names.  (Day 20)
"""

import os

from dotenv import load_dotenv

load_dotenv()  # capstone/backend/.env padho (ANTHROPIC_API_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # capstone/backend/

# --- LLM / embeddings ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-6"          # Day 21 (generation)
EMBED_MODEL = "all-MiniLM-L6-v2"            # Day 2+ (local, free)

# --- storage paths (data/ gitignored) ---
CHROMA_DIR = os.path.join(BASE_DIR, "data", "chroma")
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
COLLECTION = "smartsupport"                 # 1 collection, company_id se filter (multi-tenant)

# --- frontend origin (CORS, Day 23 React = Vite default 5173) ---
FRONTEND_ORIGIN = "http://localhost:5173"

os.makedirs(CHROMA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
