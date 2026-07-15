# 🚀 RAG Mastery — 25-Day Learning Journey

> **Retrieval-Augmented Generation ko scratch se seekhna — ek frontend developer ke nazariye se.**
> Har concept pehle **pure Python mein khud banaya**, phir library se compare kiya. No black boxes.

[![Progress](https://img.shields.io/badge/Progress-Day%205%2F25-brightgreen)]()
[![Python](https://img.shields.io/badge/Python-3.9-blue)]()
[![LLM](https://img.shields.io/badge/LLM-Claude-orange)]()

---

## 🎯 Yeh repo kya hai?

Main ek **frontend developer** (React / Angular / TypeScript) hun jo GenAI seekh raha hai.
Yeh repo meri **daily RAG learning journey** ka living record hai:

- 🛠️ **Scratch-first:** har concept (cosine similarity, chunking, vector store, persistence)
  pehle **bina kisi library ke** khud banaya — taaki magic na lage, math lage
- 📚 **Library-second:** phir wahi cheez production tool se (FAISS, ChromaDB, LangChain)
- 🔗 **Frontend analogies:** har concept ko React/JS se map kiya
  (embeddings ≈ serialization, retrieval ≈ fetch, vector DB ≈ IndexedDB, chunking ≈ pagination)
- 📝 **Har din:** code + lecture notes + SVG diagrams + self-made exercise (solved)

## 📂 Structure

```
day-XX/
├── 01_<topic>_scratch.py    # concept from scratch (no libraries)
├── 02_<topic>_library.py    # same thing with the real tool
├── notes.md                 # lecture notes + embedded diagrams
├── diagrams/*.svg           # visual explanations
└── exercise.md              # self-quiz (solved next day)

ROADMAP.md      # pura 25-din ka plan (5 phases)
PROGRESS.md     # daily tracker — kahan tak pahunche
docs/           # mentor-map, course-sync, future module blueprints
```

## 🗺️ Roadmap (5 Phases)

| Phase | Days | Focus | Status |
|-------|------|-------|--------|
| 🔵 Scratch se RAG | 1–4 | Embeddings, cosine, chunking, FAISS — sab khud banao | ✅ |
| 🟢 Dots Connect | 5–8 | ChromaDB, document loaders, retrieval quality, e2e bot | 🔄 |
| 🟡 Frameworks | 9–13 | LangChain, LlamaIndex, routing, RAGAS evaluation | ⏳ |
| 🟣 Advanced RAG | 14–18 | HyDE, re-ranking, multi-query, Agentic RAG | ⏳ |
| 🟠 Full Project | 19–25 | React/Angular + FastAPI + Chroma + Claude full-stack app | ⏳ |

## ✅ Ab tak ke highlights

- **Day 1** — RAG zero-library demo + Claude grounding (hallucination se bachav live dekha)
- **Day 2** — Cosine similarity haath se banaya, library se **exact match** (0.2746 = 0.2746)
- **Day 3** — Chunking: `step = chunk_size - overlap` khud derive kiya; overlap ka boundary-fix live
- **Day 4** — MiniVectorStore class → FAISS; dono ka **same result** = proof ki FAISS sirf fast hai, alag nahi
- **Day 5** — Persistence scratch (localStorage pattern) → ChromaDB; metadata `where` filter ne
  retrieval bug live fix kiya

## 🧰 Stack

- **LLM:** Anthropic Claude (`claude-sonnet-4-6`)
- **Embeddings:** `sentence-transformers` (all-MiniLM-L6-v2 — free, local)
- **Vector:** FAISS (in-memory index) + ChromaDB (persistent)
- **Chunking:** LangChain text splitters

## 🏃 Run karne ke liye

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # apni ANTHROPIC_API_KEY daalo
python day-01/rag_demo.py
```

## 📖 Learning ke saath-saath

Yeh journey [Coding Ninjas GenAI course](https://github.com/rahul8879/coding_ninja_genai) ke
saath synced hai — har day mentor ke notebooks se compare hota hai (`docs/mentor-map.md`).
RAG ke baad: **Agents module** (blueprint `docs/agents-roadmap-draft.md` mein ready ho raha).

---

*Building in public, ek din mein thoda — [@ranavj](https://github.com/ranavj)* 🌱
