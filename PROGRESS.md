# 📈 Progress Tracker

> Har din ke baad yeh update hoga. Naya session shuru karte waqt **yeh sabse pehle padho**.

**Current status:** ✅ Day 11 done → Next: Day 12-13 (Evaluation — RAGAS)
**Last updated:** 2026-07-21
**⚠️ Handoff note:** Teaching style = concept-FIRST, then code; frontend (React/Angular/TS) analogies; Hinglish; never dump code without explaining "why". Go SLOW, let learner predict before revealing.
**⚠️ NEXT SESSION first task:** Day 11 ka `day-11/exercise.md` learner se check karo, PHIR Day 12-13 (RAGAS eval). Weekend course pull ka overview dena (docs/course-sync.md).

---

## ✅ Completed Days

- **Day 11** — Query Routing ("receptionist"). 3 sources (HR/Finance/Tech). File1 embedding-router (cosine to source descriptions; weak model atka on "chhutti"=0.12). File2 LLM-router (Claude) nailed all incl "paisa wapas"→FINANCE (no keyword). 2-level arch: 1 ChromaDB, many collections (router=descriptions index, sources=own collections). KEY: LLM DECIDING (not just answering) = agents ki jhalak → Day 17-18 seed. Mentor session-06-07/04: RouterQueryEngine+LLMSingleSelector, QueryEngineTool (source=tool, agents vocab).

- **Day 10** — LlamaIndex (doosra framework). `Documents→VectorStoreIndex.from_documents (chunk+embed+store ek line)→as_query_engine→query()`. Same PDF+query → LlamaIndex(~4 lines) & LangChain(~10 lines) gave same answer (EMI bounce=₹1000+GST). Philosophy: LangChain=React(control), LlamaIndex=Next.js(convenience). Setup gotcha: py3.9 clash → pinned old version + bridged Claude via LangChainLLM(ChatAnthropic) into LlamaIndex. Mentor (session-06-07): 01_why(LangChain)→02_basic(LlamaIndex, SimpleDirectoryReader).

- **Day 9** — 🟡 PHASE 3 shuru: LangChain **LCEL** (`retriever|prompt|llm|parser`). Built `|` from scratch (operator overloading `__or__` = nested calls saaf). Manual RAGBot(vanilla) → declarative chain(framework). KEY: cosine/MMR/embeddings/Chroma DIDN'T vanish — packed inside `retriever`/`emb`/`Chroma()` lines (framework=wrapper). LangChain = full GenAI/Agentic framework (RAG is one part; CodeSentinel/LangGraph = same family). Mentor scam_guard: `prompt|llm|parser` + **PydanticOutputParser** (structured output = TS interface) + prompt versioning.

- **Day 8** — 🎉 PHASE 2 CAPSTONE: `RAGBot` class (ingest+ask, all 6 skills) + **Streamlit browser chat UI** (`app.py`). Tested LIVE in browser: EMI bounce → ₹1000+GST + page[2,7] citation; pizza → honest "not found" (threshold guard). Engine/UI separation (ApiClient vs component); st.session_state = React useState. Mentor bajajbot: hybrid BM25(sparse)+dense+EnsembleRetriever (Day 15 topic).

- **Day 7** — Retrieval Quality: top_k / threshold / MMR (all scratch + LangChain). Live: k=6 noise, threshold rejected 'pizza' (anti-hallucination), MMR scale-mismatch bug (lam=0.5 no effect, lam=0.1 worked). 🐛 **Caught a real bug in mentor's BFL_chatbot production config** (fetch_k==k kills MMR diversity; 'threshold' ignored in mmr mode) — the win of building scratch-first. Reused Day-6 bajaj_policy collection.

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
| 7 | 2026-07-21 | Retrieval Quality: top_k/threshold/MMR (scratch + library) | ✅ Done | 3 knobs. top_k drift (k=6 pulls credit-score/balance-transfer noise). Threshold rejects out-of-corpus query ("pizza"→"jawab nahi mila", anti-hallucination); distance-mode KAM=better vs similarity-mode ZYADA=better (tune on real scores: 0.3 wrongly rejected EMI@0.297→0.25). MMR=Maximal Marginal Relevance (thali not 3 katori daal); scratch scale-mismatch (relevance -dist vs repeat cosine, diff scales)→lam=0.5 no effect, lam=0.1 gave p7+p5+p7 diverse. 🐛 Mentor BFL_chatbot bug: fetch_k==k (no MMR choice) + threshold ignored in mmr mode. LangChain normalizes internally. Mentor 03_retreiveal = LlamaIndex (Day10). 1 diagram. Exercise solved (all correct). |
| 11 | 2026-07-21 | Query Routing (scratch embedding + LLM router) | ✅ Done | Router = receptionist / React Router (query MEANING se sahi source). 3 sources HR/Finance/Tech. File1 embedding-router (cosine to descriptions; weak model "chhutti"=0.12 atka, retrieve galat). File2 LLM-router (Claude) = all correct incl "paisa wapas"→FINANCE (no "refund" word). Arch: 1 ChromaDB many collections (router=desc index L1, sources=own collections L2; only chosen retrieved=sharp+fast). BIG: LLM DECIDING not just answering = agents jhalak (Day17-18 seed; CodeSentinel tool-choice link). Mentor 04_routing: per-source Pinecone index + QueryEngineTool(name+desc)=source-as-tool + RouterQueryEngine+LLMSingleSelector. 1 diagram. Exercise solved (all correct). |
| 10 | 2026-07-21 | LlamaIndex + LangChain-vs-LlamaIndex (framework #2) | ✅ Done | LlamaIndex mental model: Documents→VectorStoreIndex.from_documents (chunk+embed+store 1 line)→as_query_engine(similarity_top_k)→query(). File2 side-by-side same query: LangChain ~10 lines vs LlamaIndex ~4, LAGBHAG SAME answer (EMI bounce ₹1000+GST T+1). Philosophy LangChain="control do"(React) vs LlamaIndex="mujhpe chhod"(Next.js). Concepts again hidden (D2/D3/D5/D7/D1 packed). Setup gotcha: py3.9 vs latest LlamaIndex (Path|None) → pin llama-index-core==0.11.23; anthropic SDK clash → bridged via LangChainLLM(ChatAnthropic) (frameworks interconnect). Mentor session-06-07: 01_why=LangChain, 02_basic=LlamaIndex SimpleDirectoryReader+pprint_response(show_source). 1 diagram. Exercise solved (all correct). |
| 9 | 2026-07-21 | LangChain LCEL (scratch pipe + chain) | ✅ Done | `|` scratch via `__or__` operator overloading (parse(llm(prompt(retrieve(q)))) == retriever|prompt|llm|parser). Real LCEL: {context:retriever|format, question:RunnablePassthrough}|prompt|llm|parser; same behaviour as Day-8 (EMI→Rs1000+GST, pizza→"jaankari nahi"). KEY insight: Day1-8 concepts (cosine/MMR/embed/chunk/Chroma) not gone — hidden inside retriever/emb/Chroma() (framework=wrapper; scratch-first=we know inside). LangChain=full GenAI/agentic fw (RAG one part). Mentor scam_guard (production): prompt|llm|parser + PydanticOutputParser (structured/typed output) + prompt registry versioning. Analogy: vanilla JS→React. 1 diagram. Exercise solved (all correct; D1 magic-trick caught). |
| 8 | 2026-07-21 | End-to-end RAGBot + Streamlit UI (CAPSTONE) | ✅ Done | `RAGBot` class: ingest()=load+clean+chunk+store (once, persist-skip), ask()=retrieve+threshold+Claude+citations (per query, returns {answer,sources}). Streamlit `app.py` = browser chat (st.session_state=useState; script re-runs top-to-bottom). LIVE browser test: EMI bounce=Rs1000+GST @page[2,7]; pizza="jaankari nahi mili" (honest). Knobs top-of-file (config/code separation). Mentor session4_bajajbot: hardcoded Documents, HuggingFace emb, +**BM25 sparse + dense + EnsembleRetriever hybrid** (dense=meaning wins on "installment nahi de paunga", BM25=exact wins on code "BFL-PL-2024"; Day 15). 2 diagrams. Exercise solved (all correct; D1 guard-trick caught). |
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

## ▶️ Next session (Day 9 — LangChain LCEL, Phase 3 shuru 🟡)
- Phase 1+2 done (scratch + real pipeline + bot + UI). Ab Phase 3 = FRAMEWORKS.
- Day 9 goal: LangChain LCEL — `prompt | llm | parser` pipe syntax; poore RAGBot ko LCEL chain mein.
- Frontend bridge: pipe/compose (RxJS `pipe()`, unix `|`, function composition).
- Mentor: `03_prompt_engineering/Langchain_learning/` + `Projects/scam_guard/app/chain/scam_chain.py`
  (LCEL production example: prompt|llm|parser).
- Pattern same: scratch (manual chain) → LCEL → mentor compare → notes+diagram+exercise.
- IGNORE old lines below (Day 8 done).
  + Claude generation + citations, apne (ya naye) dataset pe. Yeh Phase-1/2 ka capstone.
- Mentor: `session-04/session4_bajajbot_complete.ipynb` + `Projects/BFL_chatbot/` (full structure).
- Frontend bridge: ek reusable service/module (jaise ek API client class).
- Day 6 wale bajaj_policy Chroma collection ko hi reuse karo (40 chunks ready hain).
- Mentor: `04_RAG_NLP/session-06-07/03_retreiveal.ipynb` + `Projects/BFL_chatbot/app/rag_chain.py`
  (LIVE MMR config: `k`, `fetch_k`, `lambda_mult`).
- Frontend bridge: search ranking / debounce / result de-duplication.
- Pattern same: scratch (threshold/MMR logic khud) → library → mentor compare → notes+diagram+exercise.
