# Day 20 — Backend skeleton + Ingestion pipeline (Phase 5 🟠)

> Build-day (concept-days ka scratch+library pattern ab nahi). App ka **"upload side"** bana:
> ab company PDF daale → chunk+embed hoke Chroma me chali jaaye. Sab code `capstone/backend/`.

## 🆕 FastAPI = Python ka Express/Nest
```python
@app.get("/api/health")        # ≈ app.get(...) Express me
def health(): return {"status": "ok"}   # dict → JSON auto
```
- `uvicorn app.main:app --reload` se chalta (≈ nodemon). `--reload` = file badle to auto-restart.
- **FREE bonus:** `/docs` pe Swagger UI khud ban jaata (interactive API tester).
- **Pydantic auto-validation:** route pe `response_model=UploadResponse` / body `ChatRequest` laga do →
  galat shape aayi to FastAPI khud **422** deta. = TS types, par RUNTIME pe enforce (Express me manual).

## Banaya (files)
- `app/config.py` — .env key, paths (CHROMA_DIR/UPLOAD_DIR), `COLLECTION="smartsupport"`, CORS origin.
- `app/main.py` — FastAPI app + **CORS** (React 5173 allow, Day 23 ready) + `include_router(prefix="/api")`.
- `app/api/routes.py` — `/health` + `POST /upload`.
- `app/ingestion/pipeline.py` — asli kaam (neeche).

## 🔧 Ingestion pipeline (Day 6+3+5 reuse, NAYA = tenant tag)
`ingest_pdf(file_path, company_id) -> (doc_id, n_chunks)`:
1. **LOAD** PyPDFLoader (Day 6) — har page ek Document (text+metadata)
2. **CLEAN** khali lines squeeze (Day 6; arbitrary upload isliye light, boilerplate-specific nahi)
3. **CHUNK** RecursiveCharacterTextSplitter 500/80 (Day 3) — metadata virasat
4. **STORE** Chroma (Day 5) — har chunk me `{company_id, doc_id, source, page}`
   - `doc_id = uuid4[:8]` (ek upload = ek doc_id)
   - **1 collection, company_id se filter** (multi-tenant; alag collection nahi)
   - embedding: `SentenceTransformerEmbeddingFunction(all-MiniLM-L6-v2)` — ingest+retrieval same fn

## ✅ Test (live)
- Standalone: bajaj PDF → 46 chunks; "EMI bounce" → p2 ₹1000+GST (Day 6 wala sahi jawab).
- **Multi-tenant isolation proved:** `where company_id=bajaj` → 2 hits; `company_id=acme` → **0**. 🔒
- API: `curl POST /api/upload -F file=@... -F company_id=bajaj` → `{doc_id, chunks:46, status:ok}`; Chroma=46.

## Next (Day 21) — Retrieval + Generation (RAG core as API)
`retrieval/retriever.py` (Chroma search + company_id filter + threshold, Day 7) →
`generation/rag_chain.py` (chunks + Claude → grounded answer + citations, Day 8/9) →
`POST /api/chat` (plain RAG, agent baad me Day 22) → `{answer, sources}`.

## 🐛 Future TODO (noted)
- **Dedup:** same PDF dobara upload → naye 46 chunks (duplicate). hireflow me `dedup.py` hai — Day 24 polish.
- Upload sirf PDF maan raha (validation Day 24).
