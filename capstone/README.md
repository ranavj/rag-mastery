# 🏆 SmartSupport — Agentic RAG Support Bot (Capstone)

> rag-mastery ka final project (Day 19-25). Ek company docs upload kare → **branded Q&A bot** mile,
> jiska differentiator ek **AGENT** hai jo har sawaal pe khud tool chunta hai.

**Full architecture + day-by-day plan:** [`../docs/capstone-roadmap.md`](../docs/capstone-roadmap.md)
**Kyun (vision):** [`../docs/capstone-vision.md`](../docs/capstone-vision.md)
**Picture:** [`../docs/capstone-arch.svg`](../docs/capstone-arch.svg)

---

## Agent ke 3 raaste (differentiator)
| Route | Kab | Kya |
|-------|-----|-----|
| 📄 `policy_search` | docs-related sawaal | RAG → jawab + citations |
| 🔢 `account_api` | "mera balance/EMI/order?" | live data (abhi mock) |
| 🚫 `none` | out-of-scope | honest "jaankari nahi" (no hallucination) |

## Stack
React + TypeScript (Vite) · FastAPI · Chroma · sentence-transformers · Claude · LangChain agent · RAGAS eval

## Folder map
```
backend/app/
  ingestion/  → upload→clean→chunk→embed→Chroma   (Day 6,3,2,5)
  retrieval/  → search + threshold + rerank        (Day 7,15)
  generation/ → Claude + citations                 (Day 8,9)
  agent/      → tools + AgentExecutor               (Day 17-18)
  api/        → routes (upload, chat, health)
  models/     → Pydantic schemas (API contract)
frontend/src/
  api/        → ApiClient + TS types (contract mirror)
  components/ → ChatWindow, Citation, UploadBox
  pages/      → Chat, Upload, Dashboard
```

## API contract (source of truth: `backend/app/models/schemas.py` ⇄ `frontend/src/api/types.ts`)
- `POST /api/upload` (multipart: file, company_id) → `{ doc_id, chunks, status }`
- `POST /api/chat` `{ company_id, question }` → `{ answer, sources[], tool_used }`
- `GET  /api/health` → `{ status: "ok" }`

## Status
🟢 **Day 19 done** — design + skeleton + API contract. Next: Day 20 (FastAPI + ingestion).

## Run (Day 20+ se)
```bash
# backend
cd backend && uvicorn app.main:app --reload
# frontend (Day 23+)
cd frontend && npm run dev
```
