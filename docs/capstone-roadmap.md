# 🏗️ Capstone Roadmap — SmartSupport SaaS (Day 19-25)

> **Yeh file = Phase 5 (final project) ka permanent, self-contained plan.**
> Naya context window / fresh session yahan se sab samajh sakta hai. Agar conversation
> memory chali gayi, toh `PROGRESS.md` → yeh file → `capstone-vision.md` padho, pura context wapas.
> Companion files: [`capstone-vision.md`](capstone-vision.md) (kyun), [`capstone-arch.svg`](capstone-arch.svg) (architecture picture), [`mentor-map.md`](mentor-map.md) (mentor refs).

---

## 🎯 Project ek line me
**SmartSupport** — ek RAG-as-a-Service app jahan company docs upload kare → branded Q&A bot mile,
PAR uska **differentiator = ek AGENT** jo har sawaal pe tool chunta hai:
- 📄 **policy_search** (RAG tool) → docs se jawab + citations
- 🔢 **account_api** (live data tool, abhi mock) → "mera balance/EMI/order kaha hai?"
- 🚫 **out-of-scope** → honest "yeh jaankari nahi hai" (self-correcting, no hallucination)

**Scope (imaandaar):** Day 19-25 = ek STRONG **single-tenant** version banao (upload → chat → agent →
citations → eval → deploy). Multi-tenant + auth + billing + embed widget = **post-course** extension.

**Learner ki taakat:** frontend (React/TS) 💪 → yeh project 70% full-stack + 30% RAG/agent engine.

---

## 🧰 Tech stack (LOCKED)
| Layer | Choice | Kyun / Reuse |
|-------|--------|--------------|
| Frontend | **React + TypeScript** (Vite) | Learner's ghar. Chat + upload + dashboard |
| Backend | **FastAPI** (Python) | RAG engine ko API banao (Day 8 RAGBot pattern) |
| Vector DB | **Chroma** (persistent) | Day 5-6. `company_id` metadata (multi-tenant ready) |
| Embeddings | **sentence-transformers** (all-MiniLM-L6-v2) | Day 2+, local free |
| LLM | **Claude** (`claude-sonnet-4-6`) | `.env` key, jo ab tak use kiya |
| Agent | **LangChain** `create_tool_calling_agent` + `AgentExecutor` | Day 17-18 |
| Rerank (opt) | CrossEncoder (Day 15) | eval se prove karke lagao |
| Eval | **RAGAS** (Day 12) | faithfulness / relevancy dashboard |
| Deploy | **Render** (backend) + **Vercel** (frontend) | free tier |

---

## ✅ DECIDED (locked 2026-07-28 — koi open point nahi bacha)
- **Repo:** `rag-mastery/capstone/` (learner ne choose kiya).
- **Seed corpus / first tenant:** **Bajaj policy** (Day 6 ke ready 40 chunks). NOTE: yeh sirf
  demo/test ka SEED data hai (React app ka dummy/seed data jaisa) — app ki limitation NAHI. App
  ka product hai hi "koi bhi PDF upload karo", toh baad me upload button se aur PDFs test kar sakte.
  Bajaj isliye: (1) ready+tested, (2) finance domain me `account_api` mock natural, (3) demo-ready.

## 📁 Folder structure (mentor `hireflow` style)
Base folder: **`rag-mastery/capstone/`** (decided). rag-mastery ke purane din se code copy/reuse.

```
rag-mastery/capstone/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + routes + CORS
│   │   ├── config.py            # env, settings
│   │   ├── ingestion/           # upload → clean → chunk → embed → Chroma
│   │   │   └── pipeline.py
│   │   ├── retrieval/           # Chroma search (company_id filter) + rerank
│   │   │   └── retriever.py
│   │   ├── generation/          # Claude + citations (RAG answer)
│   │   │   └── rag_chain.py
│   │   ├── agent/               # tools + AgentExecutor (Day 17-18)
│   │   │   ├── tools.py         # policy_search, account_api
│   │   │   └── agent.py
│   │   ├── api/                 # route handlers (upload, chat, health)
│   │   │   └── routes.py
│   │   └── models/              # Pydantic request/response schemas
│   │       └── schemas.py
│   ├── data/                    # chroma persist + uploaded files (gitignore)
│   ├── requirements.txt
│   └── .env                     # ANTHROPIC_API_KEY (gitignore)
├── frontend/                    # Vite + React + TS
│   ├── src/
│   │   ├── api/client.ts        # ApiClient (fetch wrapper) — TS interfaces
│   │   ├── components/          # ChatWindow, MessageList, Citation, UploadBox
│   │   ├── pages/               # Chat, Upload, Dashboard
│   │   └── App.tsx
│   └── package.json
└── README.md                    # architecture + demo + how-to-run
```

---

## 🔌 API contract (Day 19 pe final, yeh starting draft)
TS interfaces + FastAPI Pydantic — dono ka source of truth same rakho.

```ts
// POST /api/upload   (multipart: file, company_id)
interface UploadResponse { doc_id: string; chunks: number; status: "ok" | "error"; }

// POST /api/chat
interface ChatRequest  { company_id: string; question: string; }
interface Source       { text: string; page?: number; doc_id: string; }
interface ChatResponse {
  answer: string;
  sources: Source[];          // citations (agar RAG tool chala)
  tool_used: "policy_search" | "account_api" | "none";  // agent ne kya chuna
}

// GET /api/health -> { status: "ok" }
```

---

## 🗓️ Day-by-day plan (Day 19-25)

> **Build-phase workflow adapt:** concept-days wala "scratch+library 2 files" yahan lagu NAHI.
> Har build-day: (1) chhota **plan** likho, (2) code likho + test, (3) `capstone/PROGRESS` ya day-note
> update, (4) commit + push. Diagram/exercise optional (jahan naya concept ho tab).

### 📐 Day 19 — Design & Architecture (NO heavy code)
- [x] **Repo:** `rag-mastery/capstone/` (DECIDED).
- [x] **Seed corpus / first tenant:** Bajaj policy (DECIDED — seed data, changeable via upload).
- [ ] `capstone/` folder skeleton create (upar wala structure).
- [ ] **API contract final** (upar wala draft refine + TS interfaces file + Pydantic schemas).
- [ ] Data model: `company_id`, doc metadata (source, page, doc_id).
- [ ] Architecture doc (yeh file + `capstone-arch.svg` ko project README me).
- **Deliverable:** architecture doc + empty folder skeleton + API contract.
- **Mentor ref:** `coding_ninja_genai/Projects/hireflow/` (ingestion/retrieval/generation/api folders).

### 🔧 Day 20 — Backend skeleton + Ingestion pipeline
- [ ] FastAPI app (`main.py`) + CORS + `/api/health`.
- [ ] `ingestion/pipeline.py`: upload file → clean (Day 6) → chunk (Day 3) → embed → Chroma
      with `company_id` + page metadata.
- [ ] `POST /api/upload` endpoint → returns `{doc_id, chunks}`.
- [ ] Test: ek PDF upload karke Chroma me chunks verify.
- **Reuse:** Day 6 loaders + Day 3 chunking + Day 5 Chroma.
- **Deliverable:** working upload → ingest → store.

### 🔍 Day 21 — Retrieval + Generation (RAG core as API)
- [ ] `retrieval/retriever.py`: Chroma search with `company_id` filter + threshold (Day 7)
      + optional rerank (Day 15).
- [ ] `generation/rag_chain.py`: retrieved chunks + Claude → grounded answer + citations (Day 8 pattern, LCEL Day 9).
- [ ] `POST /api/chat` (plain RAG version first) → `{answer, sources}`.
- [ ] Test: "EMI bounce charge?" → sahi answer + page citation; "pizza?" → "not found".
- **Deliverable:** working RAG Q&A over API.

### 🤖 Day 22 — Agent layer (THE differentiator, Day 17-18)
- [ ] `agent/tools.py`: `policy_search` (wraps Day 21 RAG) + `account_api` (mock live data) + descriptions (LAKSHMAN REKHA — na tight na dheeli!).
- [ ] `agent/agent.py`: `create_tool_calling_agent` + `AgentExecutor`.
- [ ] `/api/chat` ko agent ke through route karo → response me `tool_used` add.
- [ ] Test: policy Q → policy_search; "mera balance?" → account_api; "mausam?" → honest "nahi pata".
- **Deliverable:** agentic /chat (3 raaste live).

### ⚛️ Day 23 — React frontend
- [ ] Vite + React + TS setup. `api/client.ts` (ApiClient, TS interfaces).
- [ ] **Chat UI:** message list + input + citations render + `tool_used` badge + loading/error/empty states.
- [ ] **Upload flow:** file input → `POST /api/upload` → status.
- [ ] (Optional) Admin dashboard stub (uploaded docs list).
- [ ] Backend se connect (CORS), end-to-end test browser me.
- **Reuse:** Day 8 Streamlit ka mental model, ab proper React (learner's home).
- **Deliverable:** working browser app (upload + chat).

### 📊 Day 24 — Eval + Polish
- [ ] RAGAS eval (Day 12) pipeline pe: faithfulness / answer_relevancy / context_precision.
- [ ] Eval report / mini dashboard (score dikhao).
- [ ] Polish: error states, "not found" honest UI, citations UX, mobile-ish responsive.
- [ ] Project `README.md`: architecture + screenshots + how-to-run.
- **Deliverable:** eval numbers + polished UX + README.

### 🚀 Day 25 — Deploy + Ship
- [ ] Backend → **Render** (FastAPI, env vars, Chroma persist).
- [ ] Frontend → **Vercel** (env = backend URL, prod CORS).
- [ ] Live smoke test (upload + chat + agent + citations).
- [ ] Final README + demo GIF/screenshots. Add to `github.com/ranavj`.
- [ ] Consolidated LinkedIn post material (see `posts/`, per project-memory plan).
- **Deliverable:** 🎉 LIVE app + repo + demo.

---

## ✅ Definition of Done (capstone)
- Live URL (Vercel frontend + Render backend) working.
- Upload → chat → **agent picks correct tool** → grounded answer + citations.
- Out-of-scope query pe honest "nahi pata" (no hallucination).
- RAGAS eval numbers in README.
- Clean repo + README + demo on `github.com/ranavj`.

## 🔗 Post-capstone extensions (future, NOT Day 19-25)
- Multi-tenant: real auth + `company_id` from session, per-tenant admin.
- Billing, embed widget (`<script>` snippet), branded themes.
- Agents module ke baad: agent jo docs khud organize kare / support auto-resolve.

---

## 🧭 FRESH SESSION — START HERE
1. `PROGRESS.md` padho → current day dekho.
2. Yeh file (`docs/capstone-roadmap.md`) → us din ka checklist uthao.
3. `capstone-vision.md` (kyun) + `capstone-arch.svg` (picture) reference.
4. Teaching style same: concept-first, Hinglish, React/TS analogy, go slow, learner predict kare.
5. Har build-day ke baad: commit + push, PROGRESS.md update.
6. Pending TODO (Phase 4 se): Day 17-18 mentor comparison (`05_Agentic_AI/` + `BFL_chatbot/app/bajaj_tools.py`).
