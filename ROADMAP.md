# 🚀 RAG Mastery — A to Z Learning Journey

> **Learner:** Vijay (Frontend Developer — React, Angular, TypeScript)
> **GitHub:** https://github.com/ranavj
> **Approach:** Build-first (scratch → frameworks → production). Har concept frontend analogy se connect hoga.
> **Mentor reference:** https://github.com/rahul8879/coding_ninja_genai (`04_RAG_module`)

---

## 📌 How this works (READ THIS FIRST every session)

- Yeh roadmap **permanent record** hai. Conversation memory khatam ho jaaye toh bhi `ROADMAP.md` + `PROGRESS.md` padhke pura context wapas aa jaata hai.
- Har din: ek `day-XX/` folder banta hai → code + notes likhe jaate hain → `PROGRESS.md` update hota hai → GitHub pe push.
- Har naya session shuru karte waqt: pehle `PROGRESS.md` padho (kahan the), phir `ROADMAP.md` ka agla pending day uthao.
- Roadmap **flexible** hai — koi topic enhance/change/add karna ho toh yeh file edit karo.

---

## 🗺️ The 5 Phases (25 days, ~thoda-thoda daily)

### 🔵 Phase 1 — Scratch se RAG (Day 1–4) — *No frameworks, pure Python*
| Day | Topic | Frontend Bridge | Deliverable |
|-----|-------|-----------------|-------------|
| 1 | RAG mental model + zero-library demo | `fetch() → render` jaisa flow | Working mini-RAG, no libs |
| 2 | Embeddings — text ko numbers banana | `JSON.stringify()` — object→string | Manual embedding + similarity |
| 3 | Chunking strategies | String split / pagination | Compare fixed vs semantic chunks |
| 4 | FAISS vector store from scratch | localStorage / IndexedDB | First full RAG pipeline |

### 🟢 Phase 2 — Dots Connect (Day 5–8) — *Mentor ke notebooks samjho*
| Day | Topic | Frontend Bridge | Deliverable |
|-----|-------|-----------------|-------------|
| 5 | ChromaDB — proper vector DB | React Query cache layer | Chroma-based retrieval |
| 6 | Document Loaders (PDF, CSV, Web) | API adapters / data services | Multi-source loader |
| 7 | Retrieval quality (Top-K, MMR, threshold) | Search ranking / debounce | Tuned retriever |
| 8 | End-to-end RAG bot (own dataset) | Full feature component | Working Q&A bot |

### 🟡 Phase 3 — Frameworks (Day 9–13) — *LangChain + LlamaIndex*
| Day | Topic | Frontend Bridge | Deliverable |
|-----|-------|-----------------|-------------|
| 9 | LangChain pipeline (LCEL) | Component composition / pipe | LangChain RAG |
| 10 | LlamaIndex — kya aur kyun | Angular vs React (alag philosophy) | LlamaIndex RAG |
| 11 | Query Routing | Router (React Router / Angular routing) | Multi-source router |
| 12-13 | Evaluation (RAGAS) | Unit/integration tests | Eval report + scores |

### 🟣 Phase 4 — Advanced RAG (Day 14–18) — *Production techniques*
| Day | Topic | Frontend Bridge | Deliverable |
|-----|-------|-----------------|-------------|
| 14 | HyDE (Hypothetical Doc Embedding) | Query preprocessing | HyDE retriever |
| 15 | Re-ranking (Cohere / cross-encoder) | Sort + filter pipeline | Re-ranked results |
| 16 | Multi-query + Parent-Child chunking | Multiple API calls / fan-out | Advanced retriever |
| 17-18 | Agentic RAG (RAG + tool use) | Conditional rendering / state machine | Self-correcting RAG |

### 🟠 Phase 5 — Full Project (Day 19–25) — *Portfolio-ready*
| Day | Topic | Stack | Deliverable |
|-----|-------|-------|-------------|
| 19-20 | Project design + decide | TS interfaces / API contract | Architecture doc |
| 21-23 | Build full-stack RAG app | React/Angular + FastAPI + Chroma + LLM | Working web app |
| 24-25 | Deploy + Evaluate + Ship | Vercel/Render + RAGAS | Live app on GitHub |

---

## 🎯 Final Outcome
Ek **GenAI-powered full-stack web app** — aapki existing frontend skill + nayi RAG skill ka combo. Portfolio piece for `github.com/ranavj`.

---

## ⚙️ Conventions
- **LLM:** TBD (Day 1 pe decide — OpenAI / Anthropic Claude)
- **Language:** Python for RAG core, TypeScript+React/Angular for final UI
- **Each day folder:** `day-XX/` → code + `notes.md`
- **Commit message format:** `Day XX: <topic>`
