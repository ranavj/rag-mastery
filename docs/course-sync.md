# 🔄 Course Sync — rag-mastery ↔ Coding Ninjas GenAI

> Do cheezein saath chal rahi hain. Yeh file batati hai kaise sync rehna hai.

---

## 📅 Do tracks

| Track | Kya | Kab | Kahan |
|-------|-----|-----|-------|
| **Coding Ninjas course** | Live lectures (breadth, course pace) | **Har Saturday + Sunday** | `/Users/vijayrana/coding_ninja_genai` |
| **rag-mastery** | Deep RAG (scratch se, roz thoda) | Weekdays (Claude ke saath) | `/Users/vijayrana/rag-mastery` |

**Goal:** dono sync rahein → RAG deeply samjho + course ki breadth → phir dono milaake **projects** banao.

---

## 📍 Course progress tracker (weekend ke baad update karo)

| Course Module | Folder | Status |
|---------------|--------|--------|
| 01 Rule → GenAI | `01_from_rule_to_genai` | ✅ done |
| 02 Training → Prompting | `02_from_training_to_prompting` | ✅ done |
| 03 Prompt Engineering | `03_prompt_engineering` | ✅ done |
| 04 RAG / NLP | `04_RAG_NLP` | ✅ done (rag-mastery iska deep version) |
| 05 Agentic AI | `05_Agentic_AI` | 🔄 chal raha — **S1** foundations, **S2** LangGraph+patterns+PEAS, **S3**: CodeSentinel agent (tools + loop) + short-term memory, **S4** (Sun 2026-07-13): **long-term memory** — CoALA ke 3 types code mein (semantic=repo standards, procedural=skills .md files, episodic=author history), PostgresStore (Neon) + **embeddings se semantic search = RAG agent ke andar!**, memory-as-tools (`search_memory`, `save_finding`), HITL `interrupt()` for sensitive tools. Notes mein agentic patterns (reflection, planning, ReAct, multi-agent GIFs), **S5** (Sat 2026-07-18): **Multi-Agent Systems (MAS)** — coordination need, types: **centralised** (orchestrator-boss = parent→child components) vs **peer-to-peer** (event bus/microservices), architecture **decision matrix** (kab single/centralised/P2P — simplest jo kaam kare), drug-discovery case study, MAS Case Study Handbook PDF. Key readings added: Anthropic "Building Effective Agents" (sir: "dont skip"), Anthropic multi-agent research system, Cisco JARVIS, **S6** (Sun 2026-07-19): **CrewAI** — pehla MAS framework. Building blocks: Agent (role/goal/backstory) + Task (description/expected_output) + Crew (process=sequential). **YAML config pattern** (agents.yaml/tasks.yaml = config-driven, logic-content separation). `kickoff_async({placeholders})`. LangGraph=low-level graph (React) vs CrewAI=high-level roles (Angular). **S6 part-2:** CrewAI `@tool` decorator (CodeSentinel jaisa), **task chaining** (multiple_tasks.yaml: return→shipping→complaint→email, har task pichhle ka output use karta = promise chain), tools **agent-level vs task-level** (convenience vs tight control). KEY: sir ke retrieve-tools abhi hardcoded strings = "fake RAG" — real app mein inke andar Chroma retrieval hoga (RAG = agent-tools ka engine!). **S6 Sunday-full:** (a) CrewAI Section-3 = agentic patterns LIVE: Planning, Reflection (self-review), Human-Input + `SerperDevTool` (internet search tool); (b) Section-4 = **Multi-Agent Collaboration** (kai agents ek complaint pe); (c) 🌟 **CodeSentinel v3 (LangGraph)** = **Supervisor/Manager pattern** — Manager node `ReviewPlan` (pydantic structured output) se decide karta kaunse specialists (security/style/test) chahiye → centralised MAS (S5 theory) ab CODE mein, dono frameworks. Note: Section 3/4 ke yaml files (planning_agent/multi_agents...) repo mein missing — reference-only abhi |

> **Agents roadmap blueprint:** `docs/agents-roadmap-draft.md` — RAG ke baad ka module, course ke saath grow ho raha. RAG FIRST, phir yeh.

> **Course paradigm (whiteboard):** Prompt Eng → Context Eng (RAG) → Harness Eng → Loop Eng.
> Aap Context Eng (RAG) pe ho; course Harness/Loop (Agents) pe badh raha.

---

## 🔗 Kaise sync rehna (har weekend ke baad)

1. Weekend lecture ke baad, `coding_ninja_genai` mein naya material aata hai.
2. Batao Claude ko "is weekend yeh padha" → Claude `course-sync.md` update karega (progress + kaunse rag-mastery day se relate karta hai).
3. Agar naya topic rag-mastery ke kisi day se judta hai → `mentor-map.md` mein add/update.
4. RAG-related ho → rag-mastery mein deep dive; Agents-related ho → Day 17-18 ke liye note kar lo.

---

## ♾️ Yeh system har FUTURE module ke liye chalega (repeatable)

Course aur aage badhega — Agents ke baad aur modules aayenge. Har naye module ka **same process**:

1. **Track** — is `course-sync.md` ki progress table mein naya module add karo (folder + status).
2. **Understand** — session ke baad Claude us module ka overview de (jaise aaj Agents S3 ka diya).
3. **Blueprint** — agar module deep learning worth hai, uska apna draft roadmap banao:
   `docs/<module>-roadmap-draft.md` (jaise `agents-roadmap-draft.md`).
4. **Map** — jahan naya module current/pichhle kaam se judta hai, `mentor-map.md` ya blueprint mein note.
5. **Merge** — har module ka seekha final **portfolio project** mein fold ho (RAG + Agents + future = ek bada system).

> **Rule:** current primary focus kabhi derail na ho. Naye module = parallel planning, jab tak current (abhi RAG) khatam na ho.

### 📦 Learning pipeline (badhta rahega)
```
RAG (primary, abhi) → Agents (draft ready) → [Module N] → [Module N+1] → ...
        └──────────────── sab ek portfolio project mein merge ────────────────┘
```

### 🎯 Core principle — HAR module teacher ke saath relate + PROJECTS bhi cover
- Har module humare **deep-learning system** se guzrega (scratch-first → library → mentor compare), na sirf theory.
- Har module ki learning **teacher ke us module** se tied rahegi (notebooks + concepts).
- **Teacher ke PROJECTS bhi cover honge** (samjho + rebuild):
  | Project | Module | Kya |
  |---------|--------|-----|
  | `Projects/BFL_chatbot` | RAG + tools | Bajaj bot, MMR retrieval, tools |
  | `Projects/scam_guard` | LangChain LCEL | prompt\|llm\|parser chain |
  | `Projects/hireflow` | RAG + eval + structure | ingestion/retrieval/generation/api — architecture reference |
  | CodeSentinel (05_Agentic_AI/session-03) | Agents | PR reviewer, LangGraph loop |
- **Rule:** ek module ka deep-dive tab "complete" jab uska mentor-project bhi samajh/rebuild ho jaye.

---

## 🚀 RAG ke baad ka plan (Phase 5 + Agents merge)

- rag-mastery **Day 17-18 (Agentic RAG)** = jahan RAG + course ke Agents milte hain.
- rag-mastery **Day 19-25** = full project. Reference: `Projects/hireflow` (architecture), `Projects/BFL_chatbot`, `Projects/scam_guard`.
- **Final vision:** ek portfolio project jo RAG (rag-mastery depth) + Agents (course) dono use kare — production structure hireflow jaisa.

---

## 📚 Agents module reading (Day 17-18 ke liye — abhi optional)
Source: `coding_ninja_genai/05_Agentic_AI/aditional_paper.md`
1. AI Agents vs Agentic AI — taxonomy (arxiv 2505.10468) ⭐ foundation
2. 7 Layers of Production Agentic AI (blog) — practical
3. LangChain Memory (docs) — jab code karo
4. CoALA — Cognitive Architectures (arxiv 2309.02427) — deep, session 3 ke baad
