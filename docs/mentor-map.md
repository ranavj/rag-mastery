# 🔗 Mentor Map — rag-mastery ↔ coding_ninja_genai

> Yeh file har rag-mastery day ko mentor repo ke exact notebooks/projects se connect karti hai.
> **Local mentor repo:** `/Users/vijayrana/coding_ninja_genai` (GitHub: rahul8879/coding_ninja_genai)
> Rule: pehle scratch version khud banao (rag-mastery), PHIR mentor ka notebook kholo aur compare karo — "maine kaise banaya vs sir ne kaise banaya".

---

## 📍 Day ↔ Mentor mapping

| rag-mastery Day | Topic | Mentor file(s) (`coding_ninja_genai/`) | Connection |
|-----|-------|----------------------------------------|------------|
| ✅ 1 | RAG mental model + zero-lib demo | `04_RAG_module/session-01/session_1_exploration.ipynb` | Same "why RAG" foundation |
| ✅ 2 | Embeddings + cosine + semantic RAG | `04_RAG_module/session-02/session_2_embedding.ipynb`, `end_end_rag.ipynb` | Humne scratch banaya; sir ne end-to-end dikhaya |
| 3 | Chunking strategies | `04_RAG_module/session-03/02_docuement_chunking.ipynb` | Fixed vs semantic chunks compare karo |
| 4 | FAISS / vector store from scratch | `04_RAG_module/session-04/01_indexing.ipynb` | Indexing kyun — scratch samajh ke notebook padho |
| 5 | ChromaDB | `04_RAG_module/session-04/02_chroma_db.ipynb`, `03_chroma_end_2_end.ipynb`, `session-05/exploring_db.ipynb` | Scratch store → proper vector DB upgrade |
| 6 | Document loaders (PDF/CSV/Web) | `04_RAG_module/session-03/01_docuemnt_loader.ipynb` | Bajaj policy PDF wahi test data hai |
| 7 | Retrieval quality (Top-K, MMR, threshold) | `04_RAG_module/session-06-07/03_retreiveal.ipynb` + `Projects/BFL_chatbot/app/rag_chain.py` | BFL_chatbot mein LIVE MMR config hai (`k`, `fetch_k`, `lambda_mult`) |
| 8 | End-to-end RAG bot (own dataset) | `04_RAG_module/session-04/session4_bajajbot_complete.ipynb` + `Projects/BFL_chatbot/` | Bajajbot = mentor ka Day-8 equivalent |
| 9 | LangChain LCEL | `03_prompt/Langchain_learning/` + `Projects/scam_guard/app/chain/scam_chain.py` | scam_guard = LCEL production example (`prompt \| llm \| parser`) |
| 10 | LlamaIndex | `04_RAG_module/session-06-07/01_why_llma_index.ipynb`, `02_basic_llama_index.ipynb` | Framework #2, alag philosophy |
| 11 | Query routing | `04_RAG_module/session-06-07/04_routing.ipynb` | Multi-source router |
| 12–13 | Evaluation (RAGAS) | `04_RAG_module/session-08/rag_assesment.ipynb` + `Projects/hireflow/generation/eval_chain.py` | hireflow mein real eval chain hai |
| 14 | HyDE | _(mentor repo mein nahi — extra topic)_ | rag-mastery bonus depth |
| 15 | Re-ranking | `Projects/hireflow/retrieval/reranker.py` + `retrieval/chain.py` | hireflow ka embed→retrieve→rerank flow yahi hai |
| 16 | Multi-query + parent-child | _(mentor repo mein nahi — extra topic)_ | rag-mastery bonus depth |
| 17–18 | Agentic RAG | `05_Agentic_AI/` + `Projects/BFL_chatbot/app/bajaj_tools.py` | RAG + tools = agent ki taraf pehla kadam |
| 19–25 | Full-stack project | `Projects/hireflow/` (architecture reference) | Ingestion/retrieval/generation/api ka folder structure copy-worthy hai |

---

## 🧭 Kaise use karna hai (har session)

1. Us din ka rag-mastery scratch version pehle banao (no peeking).
2. Phir mapping table se mentor notebook kholo — compare: kya same, kya alag, kya better.
3. Differences `day-XX/notes.md` mein "Mentor comparison" section mein likho.

## 🎯 Big picture

- **rag-mastery** = depth (scratch se samjho, roz thoda)
- **coding_ninja_genai** = breadth (course pace, production projects)
- Dono ka meeting point: **Phase 5 project** — hireflow-jaisa structure + rag-mastery ki scratch understanding = portfolio piece.
