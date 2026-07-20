# 📈 Progress Tracker

> Har din ke baad yeh update hoga. Naya session shuru karte waqt **yeh sabse pehle padho**.

**Current status:** ✅ Day 6 done → Next: Day 7 (Retrieval quality — Top-K, MMR, threshold)
**Last updated:** 2026-07-19
**⚠️ Handoff note:** Teaching style = concept-FIRST, then code; frontend (React/Angular/TS) analogies; Hinglish; never dump code without explaining "why". Go SLOW, let learner predict before revealing.
**⚠️ NEXT SESSION first task:** Day 6 ka `day-06/exercise.md` learner se check karo, PHIR Day 7 shuru. Weekend course pull ka overview dena (docs/course-sync.md).

---

## ✅ Completed Days

- **Day 6** — Document Loaders. pypdf scratch (binary→text, 12 pages) → PyPDFLoader + CLEAN step (boilerplate!) + split_documents (metadata inheritance) + Chroma → cited search (EMI bounce = Rs1000+GST, PAGE 2). Citations foundation. Mentor: CSVLoader/TextLoader; cleaning was our addition. Exercise solved.

- **Day 5** — Persistence + ChromaDB. Scratch save/load (localStorage pattern) → Chroma (persist free, metadata, where-filter fixed "din" bug live). Real bug caught: relative path → `dirname(__file__)`. Mentor: LangChain wrapper, OpenAI embeddings, Pinecone (cloud vs local).
- **Day 1** — RAG from scratch, working Claude demo + LIVE embeddings preview. Learned retrieve→augment→generate, grounding, and saw real 384-dim vectors + cosine similarity with own eyes.
- **Day 2** — Cosine similarity deep dive. Built it FROM SCRATCH (matched library exactly, 0.2746). Mithai analogy (`[meetha,teekha]`) cracked it. Then built full SEMANTIC RAG (`02_semantic_rag.py`) replacing Day 1's keyword retrieve. Saw retrieval imperfection live (weak Hinglish model picked Support over Refund due to "din"). Notes have 2 embedded SVG diagrams. Exercise SOLVED by learner (all correct).
- **Day 4** — Vector Store / FAISS. Built `MiniVectorStore` class from scratch (add + exhaustive cosine search) → then FAISS (`IndexFlatIP` + `normalize_L2` = cosine). Both gave EXACT same result (0.417 Refund) proving FAISS = same work, just fast/scalable. Concepts: index vs cache, ANN/clustering ("mohalla" trick), O(n) problem. Taught Python class→JS (`__init__`=constructor, `self`=`this`). Mentor comparison (session-04): sir showed IndexFlatL2 (distance), IndexHNSWFlat (real ANN code w/ efConstruction/efSearch), memory calc. requirements.txt now maintained. 1 diagram embedded. Exercise created.
- **Day 3** — Chunking. Learner derived `step = chunk_size - overlap` himself. Scratch char-based chunking (`01_chunking_scratch.py`) showed words breaking (`Yeh`→`Ye`+`h`) + overlap saving context live. Library `RecursiveCharacterTextSplitter` (`02_chunking_library.py`) = clean word-boundary chunks. Analogies: pagination, git diff context lines, CSS word-break. Mentor comparison done (session-03 notebook — sir also did char→word→library; learned word-based chunking as middle ground). Diagram embedded. Exercise created (learner will self-solve).

---

## 🔄 Day Log

| Day | Date | Topic | Status | Notes / Key learnings |
|-----|------|-------|--------|------------------------|
| 1 | 2026-06-29 | RAG mental model + zero-library demo + embeddings preview | ✅ Done | Concept-first session. Learner self-derived: RAG-why (LLM lacks private/fresh data, retrain too costly), retrieval, why keyword search fails ("refund" vs "paisa wapas"), embeddings = meaning→numbers, vector space (similar=near), cosine similarity. Ran `day-01/rag_demo.py` (Claude, grounding works) + `day-01/embeddings_live.py` (real 384-dim vectors; refund doc won 0.463 without the word "refund"). Noted payment scored 0.426 → scores imperfect, motivates better techniques later. See `day-01/notes.md`. |
| 2 | 2026-06-30 | Cosine similarity (scratch) + Semantic RAG | ✅ Done | Built cosine from scratch (dot/magnitude/cosine), matched library (0.2746). Mithai `[meetha,teekha]` analogy. `02_semantic_rag.py` = semantic retrieve + Claude. Live lesson: weak Hinglish model ranked Support>Refund due to word "din"; top_k=2 saved it. 2 SVG diagrams embedded in notes. Exercise solved (all correct). |
| 3 | 2026-07-07 | Chunking (scratch + library) | ✅ Done | `step = chunk_size - overlap` (learner derived). Scratch char-based (words break) vs library `RecursiveCharacterTextSplitter` (clean). Overlap = git diff context lines. Mentor comparison (session-03): sir did char→word→library; word-based chunking = middle ground. 1 SVG diagram. Exercise solved (all correct). |
| 6 | 2026-07-19 | Document Loaders (scratch + library) | ✅ Done | pypdf page-by-page (binary proof: f.read()=kachra). Dirty-data lesson: repeated header/footer → milawat vectors → CLEAN before chunk. `split_documents` = metadata VIRASAT (source+page real, Day-5 fake label ab sach). Full pipeline: PDF→load→clean→chunk(500/80, 40 chunks)→Chroma→search with PAGE citation (EMI bounce Rs1000+GST @ page 2). Mentor (session-03): TextLoader+CSVLoader multi-format; no cleaning (our addition). 1 diagram. Exercise solved (all correct). |
| 5 | 2026-07-14 | Persistence + ChromaDB (scratch + library) | ✅ Done | Scratch: MiniVectorStore + save/load (json.dump/load = localStorage pattern, .tolist() serialization). LIVE bug: relative path FileNotFoundError → `dirname(__file__)` fix. Chroma: PersistentClient (persist free), collection, add(ids/docs/metadatas), query = DISTANCE (kam=better), `where` filter ne "din" retrieval bug LIVE fix kiya. Metadata = label only (data-attributes). Mentor: LangChain Chroma wrapper + OpenAI embeddings (1536-dim match) + **Pinecone cloud DB** (local vs cloud = localStorage vs Firebase). 1 diagram. Exercise solved (all correct). |
| 4 | 2026-07-08 | Vector Store / FAISS (scratch + library) | ✅ Done | `MiniVectorStore` class scratch → FAISS `IndexFlatIP`+`normalize_L2`. Same result (0.417) = proof. Index vs cache, ANN clustering (mohalla), O(n) problem. Python class→JS (`__init__`/`self`). Mentor (session-04): IndexFlatL2, HNSW real code, memory calc. requirements.txt maintained. 1 diagram. Exercise solved (all correct; D1 trick caught). |

---

## 🧠 Decisions Made
- **Mentor map (2026-07-05):** `docs/mentor-map.md` — har day ka coding_ninja_genai notebook/project mapping. Session flow: scratch first → mentor notebook compare → notes mein "Mentor comparison" section.
- **LLM provider:** Anthropic Claude (model `claude-sonnet-4-6`). API key in `.env`.
- **Embeddings (Day 2+):** will use free local `sentence-transformers` (Anthropic has no embedding model).
- **Python:** 3.9, venv at `rag-mastery/venv/`

## ❓ Open Questions / Stuck Points
_(koi nahi abhi)_

## ▶️ Next session (Day 7 — Retrieval Quality: Top-K, MMR, threshold)
- Ab pipeline REAL hai (PDF→Chroma with page metadata) — par retrieval TUNE karna nahi seekha.
- Day 7 goal: retrieval ke quality knobs — **top_k kitna ho, similarity threshold (kachra cut),
  MMR** (diversity — same-jaise 3 chunks ki jagah alag-alag angles).
- Day 6 wale bajaj_policy Chroma collection ko hi reuse karo (40 chunks ready hain).
- Mentor: `04_RAG_NLP/session-06-07/03_retreiveal.ipynb` + `Projects/BFL_chatbot/app/rag_chain.py`
  (LIVE MMR config: `k`, `fetch_k`, `lambda_mult`).
- Frontend bridge: search ranking / debounce / result de-duplication.
- Pattern same: scratch (threshold/MMR logic khud) → library → mentor compare → notes+diagram+exercise.
