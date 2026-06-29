# Day 1 — RAG from scratch (zero libraries)

**Date:** 2026-06-29
**Goal:** RAG ka core mental model + pehla working demo (no RAG framework)

## RAG = Retrieval-Augmented Generation
Frontend analogy: `onSubmit → fetch → render`
- **Retrieve** — knowledge base se relevant chunks dhundo (`array.filter()` jaisa)
- **Augment** — woh chunks + user query ko prompt mein daalo (props pass karna)
- **Generate** — LLM (Claude) context se jawab likhe (`render(data)`)

## 3-step pipeline (rag_demo.py)
1. `KNOWLEDGE_BASE` — list of text chunks (mock data / API response)
2. `retrieve(query, top_k)` — keyword overlap se top chunks (NAIVE search)
3. `ask_claude(query, chunks)` — context-grounded prompt → Claude → answer

## Key takeaways
- **Grounding:** prompt mein bola "sirf context se jawab do" → Claude ne missing info pe
  jhooth nahi banaya, "jaankari nahi hai" bola. **Yahi RAG ka anti-hallucination fayda.**
- **Limitation:** keyword match sirf exact shabd pakadta hai. "refund" likha hai par koi
  "paisa wapas" puche toh fail. → **Day 2 mein embeddings se theek karenge (semantic search).**

## Stack
- Python 3.9 + venv
- `anthropic` SDK (model: claude-sonnet-4-6)
- `python-dotenv` for API key
- API key `.env` mein (gitignored — kabhi push nahi hoga)

## Run
```bash
source venv/bin/activate
python day-01/rag_demo.py
```
