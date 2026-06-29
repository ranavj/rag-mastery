# 📈 Progress Tracker

> Har din ke baad yeh update hoga. Naya session shuru karte waqt **yeh sabse pehle padho**.

**Current status:** ✅ Day 1 done (+ embeddings preview) → Next: Day 2 (Embeddings deep dive + build)
**Last updated:** 2026-06-29
**⚠️ Handoff note:** Learner is now continuing from the **VS Code Claude extension**. This file + ROADMAP.md + memory are the source of truth. Teaching style = concept-FIRST, then code; frontend (React/Angular/TS) analogies; Hinglish; never dump code without explaining the "why".

---

## ✅ Completed Days

- **Day 1** — RAG from scratch, working Claude demo + LIVE embeddings preview. Learned retrieve→augment→generate, grounding, and saw real 384-dim vectors + cosine similarity with own eyes.

---

## 🔄 Day Log

| Day | Date | Topic | Status | Notes / Key learnings |
|-----|------|-------|--------|------------------------|
| 1 | 2026-06-29 | RAG mental model + zero-library demo + embeddings preview | ✅ Done | Concept-first session. Learner self-derived: RAG-why (LLM lacks private/fresh data, retrain too costly), retrieval, why keyword search fails ("refund" vs "paisa wapas"), embeddings = meaning→numbers, vector space (similar=near), cosine similarity. Ran `day-01/rag_demo.py` (Claude, grounding works) + `day-01/embeddings_live.py` (real 384-dim vectors; refund doc won 0.463 without the word "refund"). Noted payment scored 0.426 → scores imperfect, motivates better techniques later. See `day-01/notes.md`. |

---

## 🧠 Decisions Made
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
