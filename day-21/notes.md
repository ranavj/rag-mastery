# Day 21 — Retrieval + Generation → POST /api/chat (Phase 5 🟠)

> Build-day. App ka **"answer side"**: upload (Day 20) ho gaya, ab us data pe sawaal.
> Aaj **koi naya RAG concept nahi** — pura din purane skills ka WIRING (Day 7 + Day 8 + Day 9)
> ab API modules ke andar. Isliye fast gaya.

## Threshold — pehle probe, phir tune (Day 7 ka asli sabak)
Hardcode nahi kiya. Real distances dekhe (Chroma = distance, KAM = better):
| Query | top distance | corpus me? |
|-------|-------------|-----------|
| EMI bounce | 0.497 | ✅ |
| foreclosure | 0.423 | ✅ |
| pizza | 0.861 | ❌ |
| weather | 0.809 | ❌ |

In-corpus ~0.42-0.56, out ~0.81+ → gap me **`DISTANCE_THRESHOLD = 0.7`**. "pizza/weather" apne-aap reject.

## Files banaye
- `retrieval/retriever.py` — `retrieve(question, company_id, k=4)`:
  Chroma `query` + `where={"company_id": ...}` (tenant isolation) + threshold filter →
  `[{text, page, doc_id, distance}]` (khaali = kuch relevant nahi).
- `generation/rag_chain.py` — `answer(question, company_id) -> (text, sources)`:
  - **DOUBLE grounding guard:** (1) retriever khaali de → `NOT_FOUND`; (2) prompt Claude ko
    context ke bahar jaane se rokta (chunk aaye par jawab na ho tab bhi honest).
  - LCEL: `prompt | ChatAnthropic | StrOutputParser` (Day 9). temperature=0.
  - sources = citations (text[:200] + page + doc_id).
- `api/routes.py` — `POST /chat`: `answer()` call → `ChatResponse{answer, sources, tool_used}`.
  - **tool_used** abhi manual: sources mile → `"policy_search"`, warna `"none"`.
    (Day 22 me AGENT asli decide karega — abhi plain RAG.)

## ✅ Test LIVE (curl /api/chat)
- "EMI bounce charge?" → ₹1,000+GST, citations p7+p2, `tool_used: policy_search` ✅
- "Pizza kaise order karu?" → "jaankari nahi mili", `sources: []`, `tool_used: none` ✅ (no hallucination)

## Gotchas
- Python 3.9 f-string me `\` nahi chalta (nested quotes se bacho).
- Duplicate citations (p7,p7,p2,p2) = wahi 92 duplicate chunks (dedup future-TODO, Day 24).
- `--reload` server file badalne pe khud restart karta — dev me handy.

## Next (Day 22) — Agent layer (THE differentiator, Day 17-18)
`agent/tools.py`: `policy_search` (aaj ka RAG wrap) + `account_api` (mock live: balance/EMI/order) +
descriptions (LAKSHMAN REKHA). `agent/agent.py`: `create_tool_calling_agent` + `AgentExecutor`.
`/api/chat` ko agent ke through route → `tool_used` ab ASLI (agent ne chuna). Test: policy Q→policy_search,
"mera balance?"→account_api, "mausam?"→honest none.
