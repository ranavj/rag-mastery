# Day 22 — Agent layer (THE differentiator, Day 17-18) (Phase 5 🟠)

> Build-day. Kal tak `/api/chat` me flow SEEDHA tha (har sawaal → RAG → jawab), `tool_used`
> HARDCODE tha. Aaj asli **agent** laga: LLM khud chunta kaunsa tool. Ye capstone ka USP.

## Concept: seedhi rassi → agent loop (Day 17-18 recap)
- Seedha: sawaal → RAG → jawab (har baar same).
- Agent: LLM sochta "kaunsa tool?" → tool chalta → result wapas LLM → phir final jawab.
  `tool_used` ab **DECISION** hai, hardcode nahi.
- 3 raaste: `policy_search` (docs) / `account_api` (live data) / `none` (honest — Day8 threshold
  + Day12 faithfulness ab agent ke andar).

## 🔑 Design challenge — tool ko sirf STRING milti, par...
Agent `policy_search("EMI charge")` bulata — sirf ek string. Par tool ko `company_id`
(multi-tenant) + citations wapas chahiye. **Solution: FACTORY + closure** (React `useCallback`
dependency close-over jaisa):
```python
def build_tools(company_id, state):     # per-request
    @tool
    def policy_search(query): 
        text, sources = rag_answer(query, company_id)   # company_id closure me bound
        state["sources"] = sources                      # citations state me capture
        return text
    @tool
    def account_api(account_id): ...
    return [policy_search, account_api]
```
- `agent.py`: `create_tool_calling_agent(llm, tools, prompt)` + `AgentExecutor(return_intermediate_steps=True)`.
- **tool_used kaise pata:** `result["intermediate_steps"]` → har step ka `action.tool` (agent ne asli kya chalaya).
- Descriptions = **LAKSHMAN REKHA** (Day 17-18): policy_search="general policy, account NAHI",
  account_api="specific user ka live data, general NAHI" → agent sahi chunta.

## 🐛 Bug + fix (real catch)
Claude ka final output kabhi **string** nahi, **list-of-content-blocks** hota → `.replace` crash
+ `ChatResponse.answer` (str) fail. FIX: `_as_text()` — list ho to text blocks join.

## Files
- `agent/tools.py` — policy_search (Day 21 RAG wrap) + account_api (mock `_FAKE_ACCOUNTS`: VJ-100/VJ-200).
- `agent/agent.py` — run_agent(q, company_id) → (answer, sources, tool_used). `_as_text` normalize.
- `api/routes.py` — `/chat` ab `run_agent` call karta (plain `answer()` hata).

## ✅ Test LIVE (/api/chat, teeno raaste)
| Query | tool_used | Result |
|-------|-----------|--------|
| "EMI bounce charge?" | `policy_search` | ₹1000+GST + cite p2,p7 |
| "VJ-100 ka balance?" | `account_api` | account data (₹12,500) |
| "Mumbai mausam?" | `none` | honest refusal (no hallucination) |

## Next (Day 23) — React frontend ⚛️ (learner ka ghar 🏠)
Vite + React + TS. `api/client.ts` (ApiClient, types.ts use). Chat UI (message list + input +
citations + `tool_used` badge + loading/error/empty). Upload flow. CORS se connect, browser e2e test.
Backend ab READY — sirf UI banani hai.
