# 🤖 Agents Mastery — Roadmap DRAFT (next module after RAG)

> **Status:** DRAFT — grows as Coding Ninjas Agents module progresses (Sat/Sun lectures).
> **Priority:** RAG mastery FIRST (finish to peak). Yeh sirf blueprint hai taaki RAG ke baad ready mile.
> **CONFIRMED format (learner, 2026-07-13):** RAG-mastery jaisa hi **20-25 din ka day-by-day roadmap** banega —
> apna repo/folder, har day: scratch file + library file + notes.md + SVG diagrams + exercise.md,
> PROGRESS.md tracker, GitHub push, mentor compare. Jab RAG Day ~16 pe ho, is draft se final ROADMAP.md banayenge.
> **Style (same as rag-mastery):** scratch-first → library → mentor compare; frontend (React/Angular/TS) analogies; Hinglish; daily notes + diagram + exercise.
> **Mentor source:** `coding_ninja_genai/05_Agentic_AI/`

---

## 🧭 Big idea (whiteboard paradigm)
`Prompt Eng → Context Eng (RAG ✅) → Harness Eng → Loop Eng (Agents)`
RAG = one-shot (retrieve→generate). **Agent = LOOP** (soch → tool → soch → ... → done).

---

## 📚 Course coverage so far (seed for roadmap)

| Course Session | Topic | Key ideas |
|----------------|-------|-----------|
| S1 Foundations | AI agent kya hai | properties, evolution (rule→learning→LLM-powered), "do you really need an agent?" |
| S2 LangGraph + patterns | loop banane ka framework | StateGraph, conditional routing, **ReAct**, patterns: prompt-chaining, routing, parallelization, orchestrator-worker, evaluator-optimizer. **PEAS** design card. |
| S3 Real agent + memory | CodeSentinel (PR reviewer) | tools (sensors/actuators), agent↔tools LOOP (`should_continue`), **short-term memory** (MemorySaver + thread_id), HITL |
| S4 Long-term memory | CodeSentinel v2 | CoALA 3 memory types in code: **semantic** (standards), **procedural** (skills .md), **episodic** (author history). PostgresStore+embeddings (**memory = RAG!**), memory-as-tools, HITL `interrupt()` for sensitive tools |

---

## 🗺️ Draft phases (will refine as course continues)

### Phase A — Agent Foundations (scratch)
- Agent = LLM + tools + loop. Scratch: ek chhota "tool-calling loop" bina framework (pure Python while-loop).
- Concept: ReAct (Reason + Act). PEAS se ek agent design karo.
- Frontend bridge: while-loop + state machine (XState jaisa).

### Phase B — LangGraph (library)
- StateGraph, nodes, conditional edges = agent flow.
- Rebuild scratch agent in LangGraph. Compare (jaise RAG mein scratch vs FAISS).
- Frontend bridge: flowchart / state machine.

### Phase C — Tools + Memory
- Custom tools banao (@tool). Short-term memory (thread_id = session id).
- HITL (human approval before risky actions).

### Phase D — Agentic RAG (🔗 RAG + Agents MERGE)
- Agent ka ek tool = RAG retrieval. **Yeh rag-mastery Day 17-18 se overlap karta hai!**
- Self-correcting / decide-when-to-retrieve.

### Phase E — Multi-agent (Agentic AI)
- Single agent → multiple coordinated agents (orchestrator-worker).
- Reading: AI Agents vs Agentic AI (taxonomy), 7-layers, CoALA.

### Phase F — Full Project (CONFIRMED: learner wants CodeSentinel-jaisa apna project)
- Same ingredients: tools + LangGraph loop + 3-type memory + RAG (rag-mastery skill!) + HITL.
- **Project ideas (decide later):**
  1. **Frontend Code Reviewer** ⭐ — React/Angular/TS PRs review kare (learner ki frontend expertise + RAG + agents = unique portfolio)
  2. Docs Assistant Agent — company docs RAG + actions
  3. Bug Triager — issues categorize + author memory
- Reference: CodeSentinel (session-03/04), `Projects/BFL_chatbot` (tools), `Projects/hireflow` (structure).

---

## ⏭️ Next update
Har weekend lecture ke baad yeh file refine hogi (naye sessions → phases sharpen).
Jab rag-mastery Day 16 khatam ho, is draft ko final `agents-mastery/ROADMAP.md` bana denge.
