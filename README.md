# 🚀 RAG Mastery — A 25-Day Learning Journey

> **Learning Retrieval-Augmented Generation from scratch — through a frontend developer's lens.**
> Every concept is first built in **pure Python by hand**, then compared with the real library. No black boxes.

[![Progress](https://img.shields.io/badge/Progress-Day%2014%2F25-brightgreen)]()
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
| 🟣 Advanced RAG | 14–18 | HyDE, re-ranking, multi-query, Agentic RAG | 🔄 |
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

## 🧰 Stack

- **LLM:** Anthropic Claude (`claude-sonnet-4-6`)
- **Embeddings:** `sentence-transformers` (all-MiniLM-L6-v2 — free, local)
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
