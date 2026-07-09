# 📈 Progress Tracker

> Har din ke baad yeh update hoga. Naya session shuru karte waqt **yeh sabse pehle padho**.

**Current status:** ✅ Day 3 done → Next: Day 4 (FAISS / vector store from scratch)
**Last updated:** 2026-07-07
**⚠️ Handoff note:** Teaching style = concept-FIRST, then code; frontend (React/Angular/TS) analogies; Hinglish; never dump code without explaining "why". Go SLOW, let learner predict before revealing.
**⚠️ NEXT SESSION first task:** Day 3 ka `day-03/exercise.md` learner se check karo (unhone khud solve kiya hai), PHIR Day 4 shuru.

---

## ✅ Completed Days

- **Day 1** — RAG from scratch, working Claude demo + LIVE embeddings preview. Learned retrieve→augment→generate, grounding, and saw real 384-dim vectors + cosine similarity with own eyes.
- **Day 2** — Cosine similarity deep dive. Built it FROM SCRATCH (matched library exactly, 0.2746). Mithai analogy (`[meetha,teekha]`) cracked it. Then built full SEMANTIC RAG (`02_semantic_rag.py`) replacing Day 1's keyword retrieve. Saw retrieval imperfection live (weak Hinglish model picked Support over Refund due to "din"). Notes have 2 embedded SVG diagrams. Exercise SOLVED by learner (all correct).
- **Day 3** — Chunking. Learner derived `step = chunk_size - overlap` himself. Scratch char-based chunking (`01_chunking_scratch.py`) showed words breaking (`Yeh`→`Ye`+`h`) + overlap saving context live. Library `RecursiveCharacterTextSplitter` (`02_chunking_library.py`) = clean word-boundary chunks. Analogies: pagination, git diff context lines, CSS word-break. Mentor comparison done (session-03 notebook — sir also did char→word→library; learned word-based chunking as middle ground). Diagram embedded. Exercise created (learner will self-solve).

---

## 🔄 Day Log

| Day | Date | Topic | Status | Notes / Key learnings |
|-----|------|-------|--------|------------------------|
| 1 | 2026-06-29 | RAG mental model + zero-library demo + embeddings preview | ✅ Done | Concept-first session. Learner self-derived: RAG-why (LLM lacks private/fresh data, retrain too costly), retrieval, why keyword search fails ("refund" vs "paisa wapas"), embeddings = meaning→numbers, vector space (similar=near), cosine similarity. Ran `day-01/rag_demo.py` (Claude, grounding works) + `day-01/embeddings_live.py` (real 384-dim vectors; refund doc won 0.463 without the word "refund"). Noted payment scored 0.426 → scores imperfect, motivates better techniques later. See `day-01/notes.md`. |
| 2 | 2026-06-30 | Cosine similarity (scratch) + Semantic RAG | ✅ Done | Built cosine from scratch (dot/magnitude/cosine), matched library (0.2746). Mithai `[meetha,teekha]` analogy. `02_semantic_rag.py` = semantic retrieve + Claude. Live lesson: weak Hinglish model ranked Support>Refund due to word "din"; top_k=2 saved it. 2 SVG diagrams embedded in notes. Exercise solved (all correct). |
| 3 | 2026-07-07 | Chunking (scratch + library) | ✅ Done | `step = chunk_size - overlap` (learner derived). Scratch char-based (words break) vs library `RecursiveCharacterTextSplitter` (clean). Overlap = git diff context lines. Mentor comparison (session-03): sir did char→word→library; word-based chunking = middle ground. 1 SVG diagram. `exercise.md` pending learner self-solve. |

---

## 🧠 Decisions Made
- **Mentor map (2026-07-05):** `docs/mentor-map.md` — har day ka coding_ninja_genai notebook/project mapping. Session flow: scratch first → mentor notebook compare → notes mein "Mentor comparison" section.
- **LLM provider:** Anthropic Claude (model `claude-sonnet-4-6`). API key in `.env`.
- **Embeddings (Day 2+):** will use free local `sentence-transformers` (Anthropic has no embedding model).
- **Python:** 3.9, venv at `rag-mastery/venv/`

## ❓ Open Questions / Stuck Points
_(koi nahi abhi)_

## ▶️ Next session (Day 2) — start here in VS Code
- `sentence-transformers` ALREADY installed; `day-01/embeddings_live.py` already shows the basics.
- Day 2 goal: go deeper + BUILD — replace Day 1's keyword `retrieve()` with embedding-based semantic retrieve. Make a reusable `embed()` + `search()` over a bigger doc set.
- Then connect it to Claude (like `rag_demo.py` but with semantic retrieval) → full semantic RAG.
- Keep concept-first; let the learner predict/guess before revealing.
