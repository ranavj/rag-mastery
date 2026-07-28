# 🚀 RAG Mastery — A 25-Day Learning Journey

> **Learning Retrieval-Augmented Generation from scratch — through a frontend developer's lens.**
> Every concept is first built in **pure Python by hand**, then compared with the real library. No black boxes.

[![Progress](https://img.shields.io/badge/Progress-Day%2023%2F25-brightgreen)]()
[![Python](https://img.shields.io/badge/Python-3.9-blue)]()
[![LLM](https://img.shields.io/badge/LLM-Claude-orange)]()

---

## 🎯 What is this repo?

I'm a **frontend developer** (React / Angular / TypeScript) learning GenAI.
This repo is the living record of my **daily RAG learning journey**:

- 🛠️ **Scratch-first:** every concept (cosine similarity, chunking, vector stores, persistence)
  is built **without any library first** — so it feels like math, not magic
- 📚 **Library-second:** then the same thing with production tools (FAISS, ChromaDB, LangChain)
- 🔗 **Frontend analogies:** every concept mapped to React/JS ideas
  (embeddings ≈ serialization, retrieval ≈ fetch, vector DB ≈ IndexedDB, chunking ≈ pagination)
- 📝 **Every day ships:** code + lecture notes + SVG diagrams + a self-made exercise (solved)

## 📂 Structure

```
day-XX/
├── 01_<topic>_scratch.py    # concept from scratch (no libraries)
├── 02_<topic>_library.py    # same thing with the real tool
├── notes.md                 # lecture notes + embedded diagrams
├── diagrams/*.svg           # visual explanations
└── exercise.md              # self-quiz (solved the next day)

ROADMAP.md      # the full 25-day plan (5 phases)
PROGRESS.md     # daily tracker — where the journey stands
docs/           # mentor-map, course-sync, future module blueprints
```

## 🗺️ Roadmap (5 Phases)

| Phase | Days | Focus | Status |
|-------|------|-------|--------|
| 🔵 RAG from Scratch | 1–4 | Embeddings, cosine, chunking, FAISS — all hand-built | ✅ |
| 🟢 Connecting the Dots | 5–8 | ChromaDB, document loaders, retrieval quality, e2e bot | ✅ |
| 🟡 Frameworks | 9–13 | LangChain, LlamaIndex, routing, RAGAS evaluation | ✅ |
| 🟣 Advanced RAG | 14–18 | HyDE, re-ranking, multi-query, Agentic RAG | ✅ |
| 🟠 Full Project | 19–25 | React/Angular + FastAPI + Chroma + Claude full-stack app | ⏳ |

## ✅ Highlights so far

- **Day 1** — Zero-library RAG demo + Claude grounding (watched hallucination-prevention work live)
- **Day 2** — Built cosine similarity by hand; **exact match** with the library (0.2746 = 0.2746)
- **Day 3** — Chunking: derived `step = chunk_size - overlap` myself; saw overlap fix the boundary problem live
- **Day 4** — Built a MiniVectorStore class → FAISS; both gave the **same result** — proof that FAISS is just faster, not different
- **Day 5** — Persistence from scratch (the localStorage pattern) → ChromaDB; a metadata `where` filter
  fixed a real retrieval bug live
- **Day 6** — The pipeline got REAL: loaded an actual 12-page PDF (pypdf → PyPDFLoader), added a
  cleaning step for repeated headers, and got **cited search results** — the exact answer with its page number
- **Day 7** — Retrieval tuning (top_k, similarity threshold, MMR) from scratch; threshold taught the bot
  to say *"not found"* instead of hallucinating — and building MMR by hand let me **catch a real bug in the
  mentor's production config** (`fetch_k == k` silently kills diversity)
- **Day 8** — 🎉 **Phase 2 capstone:** wrapped all six skills into a reusable `RAGBot` class
  (`ingest()` + `ask()`) and gave it a **Streamlit browser chat UI** — a working RAG app that answers from
  a real PDF *with page citations*, and honestly says "not found" when the answer isn't there
- **Day 9** — 🟡 **Phase 3 (frameworks):** rebuilt the whole RAG flow as a LangChain **LCEL chain**
  (`retriever | prompt | llm | parser`) — after first building the `|` pipe *from scratch* with operator
  overloading, so the framework reads as a shortcut, not a black box (vanilla-JS → React, for RAG)
- **Day 10** — Rebuilt the same RAG with **LlamaIndex** and ran both frameworks side-by-side on one
  query — same answer, ~4 lines vs ~10. LangChain = React (control), LlamaIndex = Next.js (convenience);
  a good engineer knows when to reach for each
- **Day 11** — **Query routing** across 3 knowledge sources: an embedding router (from scratch) vs an
  LLM router (Claude picking the source). The moment the LLM *decides* instead of just *answers* is the
  first taste of agents — the seed of Agentic RAG
- **Day 12-13** — **Evaluation** with RAGAS — a report card for RAG. Built an LLM-as-judge from scratch,
  then ran real RAGAS metrics (faithfulness / relevancy / context precision). Faithfulness caught a
  hallucinated answer with a hard **0.00** — turning "looks right" into a number you can track
- **Day 14** — 🟣 **Phase 4 (advanced):** **HyDE** — instead of searching the raw query, ask the LLM for a
  hypothetical answer first and search *that*. A casual query that wrongly matched "Shipping" jumped to the
  right "Refund" doc (0.52). The hypothetical can be wrong and still work — it's for finding, not answering
- **Day 15** — **Re-ranking** (2-stage retrieval): a fast bi-encoder builds a rough shortlist, then a slow
  cross-encoder re-scores each *query+doc pair together* and re-sorts. Building it by hand surfaced three
  honest lessons — a good bi-encoder often nails top-1 on clean data (re-ranking is optional), re-ranking
  can even make things *worse* (I caught it demoting the right answer live), and reranker quality matters
  (a small model failed where a bigger one fixed the flip). The takeaway is the same as HyDE: **prove it with eval**
- **Day 16** — **Multi-Query + Parent-Child chunking.** Multi-Query fans one question into several LLM-worded
  variants, searches all, and merges (higher recall). Parent-Child splits twice — small *children* get embedded
  and searched (precise), but the matched child's *parent* (the full paragraph) is fetched from a side docstore
  and handed to the LLM (full context). "Search the child, return the parent." Building both from scratch also
  caught a real library bug: `MultiQueryRetriever`'s default parser turned the LLM's *"Here are 3 versions:"*
  preamble into a query — fixed with a custom output parser
- **Day 17-18** — 🎉 **Phase 4 finale: Agentic RAG.** RAG stops being a straight pipe and becomes *one tool*
  in an agent's hands. The LLM now **decides** which tool to call and with what input — policy questions go
  to the RAG tool, live-account questions to an API tool, out-of-scope questions get an honest "don't know".
  Built the agent loop from scratch first (the LLM emits a raw string → we *parse* it → call the real Python
  function), then the same loop via LangChain's `AgentExecutor`. Two live experiments on tool descriptions:
  a *lying* description often fails to fool Claude (it cross-checks name + all tools), but an *under-scoped*
  one starves the tool and triggers a hallucination — so a description is the tool's boundary line
- **Day 19** — 🟠 **Phase 5 (capstone) starts: design & architecture.** No heavy code — a blueprint day.
  Locked the decisions (repo `capstone/`, Bajaj policy as seed corpus) and scaffolded **SmartSupport**, an
  agentic RAG support bot: a hireflow-style `capstone/` skeleton (backend `ingestion/retrieval/generation/agent/api/models`
  + a React/TS `frontend/`), each backend module carrying a docstring for which day fills it and which past day
  it reuses. Core idea: the **API contract as a single source of truth** — Pydantic `schemas.py` mirrored by
  TypeScript `types.ts`, three endpoints (`/api/upload`, `/api/chat` → `{answer, sources, tool_used}`, `/api/health`)
- **Day 20** — 🟠 **Backend + ingestion pipeline.** Stood up the FastAPI backend (CORS, `/api/health`, auto
  Swagger docs) and the ingestion pipeline: a PDF upload flows through load → clean → chunk (Day 3) → embed →
  Chroma (Day 5), tagging every chunk with `company_id`, `doc_id`, and page. One collection filtered by
  `company_id` = multi-tenant isolation. `POST /api/upload` returns `{doc_id, chunks}` — tested live on the
  Bajaj PDF (46 chunks; a `company_id=acme` query returns nothing, proving the isolation)
- **Day 21** — 🟠 **RAG core as an API (`POST /api/chat`).** No new RAG concept — pure wiring of earlier skills.
  `retrieval/retriever.py` searches Chroma with a `company_id` filter and a distance threshold (0.7, *tuned by
  probing real scores* — in-corpus ~0.5, out-of-corpus ~0.85). `generation/rag_chain.py` feeds the chunks to
  Claude via an LCEL chain with a double grounding guard, returning a grounded answer plus page citations.
  Live: "EMI bounce charge?" → ₹1,000+GST with citations; "pizza?" → an honest "not found"
- **Day 22** — 🟠 **The agent layer — the capstone's differentiator.** `/api/chat` stops being a straight RAG
  pipe: an agent now *decides* which tool to use. `agent/tools.py` exposes `policy_search` (wrapping Day 21's
  RAG) and a mock `account_api` (live balance/EMI/status), each with a carefully scoped description. A
  factory binds `company_id` into the tools via closure and captures citations through a shared state dict.
  `create_tool_calling_agent` + `AgentExecutor` run the loop, and the real `tool_used` is read from the
  intermediate steps. Live: policy questions → `policy_search`, "VJ-100 balance?" → `account_api`, "today's
  weather?" → an honest "none" — no hallucination
- **Day 23** — 🟠 **React + TypeScript frontend — the app is now full-stack.** A Vite/React/TS client
  (`capstone/frontend/`) with an upload box and a chat window. The Day-19 `types.ts` contract pays off here:
  imported straight into a typed `fetch` client, so responses need zero guessing. Each answer renders the real
  `tool_used` as a colored badge (green `policy_search` / amber `account_api` / red `none`) plus page-citation
  chips — the agent's decision made visible. Verified end-to-end in the browser: React → FastAPI → agent →
  Claude → typed response → rendered

## 🧰 Stack

- **LLM:** Anthropic Claude (`claude-sonnet-4-6`)
- **Embeddings:** `sentence-transformers` (all-MiniLM-L6-v2 — free, local)
- **Re-ranking:** `sentence-transformers` CrossEncoder (ms-marco-MiniLM-L-12-v2) + LangChain reranker wrappers
- **Vectors:** FAISS (in-memory index) + ChromaDB (persistent)
- **Chunking:** LangChain text splitters
- **Loaders:** pypdf + LangChain community loaders (PDF → text + page metadata)

## 🏃 Getting started

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # add your ANTHROPIC_API_KEY
python day-01/rag_demo.py
```

## 📖 Learning alongside

This journey runs in sync with the [Coding Ninjas GenAI course](https://github.com/rahul8879/coding_ninja_genai) —
each day is compared against the mentor's notebooks (`docs/mentor-map.md`).
Up next after RAG: the **Agents module** (blueprint brewing in `docs/agents-roadmap-draft.md`).

---

*Building in public, a little every day — [@ranavj](https://github.com/ranavj)* 🌱
