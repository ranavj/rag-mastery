# Day 10 — Exercise 📝

> **Rule:** Khud solve karo. Answers `**Mera jawab:**` ke aage likho. Notes dekhna allowed.
> Kal (Day 11 se pehle) submit karna.

---

## 🧮 A. Reasoning

**A1.** LlamaIndex mein `VectorStoreIndex.from_documents(docs)` ek line hai. Yeh ek line
Day 1-8 ke kaunse-kaunse concepts andar-andar karti hai? (kam se kam 3 batao)
**Mera jawab:**
-- yeh ek line andar-andar 3 kaam karti hai:
   1. CHUNK — documents ko tukdo me todna (Day 3)
   2. EMBED — har chunk ko vector banana (Day 2, Settings.embed_model)
   3. STORE — vectors ko index me rakhna (Day 5, default in-memory)
-- framework ne teeno chhupa diye ek line me (wrapper, replacement nahi)
**A2.** Same PDF, same query se LangChain aur LlamaIndex dono ne lagbhag same jawab diya.
Iska kya matlab hai — RAG "kaunsa framework use kiya" pe depend karta hai ya kisi aur cheez pe?
**Mera jawab:**
-- same jawab = proof ki framework sirf WRAPPER hai, quality uspe depend NAHI karti
-- RAG ki quality asli components pe depend karti:
   embedding model + chunking + retrieval tuning (top_k/threshold) + data + LLM
-- dono framework me yeh sab SAME the (all-MiniLM, ~500 chunk, top_k=3, same PDF, Claude)
   -> isliye same jawab
-- lesson: "achha framework" ≠ "achha RAG". Achhe components + tuning = achha RAG
   (framework badalne se quality nahi badalti — React/Next.js dono se same app)

## 💻 B. Coding

**B1.** LangChain aur LlamaIndex mein se kaunsa "kam code" mein RAG banata hai aur kaunsa
"zyada control" deta hai? Ek-ek line se dono ka API dikhao.
**Mera jawab:**
-- LlamaIndex = KAM CODE (framework sab sambhale, "mujhpe chhod do"):
   index = VectorStoreIndex.from_documents(docs); index.as_query_engine().query(q)
-- LangChain = ZYADA CONTROL (pieces khud jodo, "control do mujhe"):
   chain = retriever | prompt | llm | parser; chain.invoke(q)
-- LangChain me har piece alag (retriever/prompt/llm/parser) -> zyada tune/customize
   LlamaIndex me sab .query() me packed -> kam code, kam control

**B2.** Humein LlamaIndex ke Anthropic wrapper mein version-clash mila. Humne use kaise
solve kiya? (frameworks ko jodne wali trick)
**Mera jawab:**
-- problem: LlamaIndex ka anthropic wrapper humare `anthropic` SDK version se clash kar raha tha
-- fix (jodne wali trick): Day-9 ka LangChain wala `ChatAnthropic` (jo already kaam kar raha tha)
   ko `LangChainLLM(ChatAnthropic(...))` se LlamaIndex me PLUG kar diya
-- yani ek framework (LlamaIndex) ne doosre framework (LangChain) ka LLM use kiya
-- lesson: frameworks alag-thalag nahi — aapas me INTERCONNECT hote hain

## ✍️ C. Text / Short answer

**C1.** LangChain = React, LlamaIndex = Next.js — is analogy ko apne shabdon mein samjhao.
Kab React (LangChain) aur kab Next.js (LlamaIndex) chunoge?
**Mera jawab:**
-- React (LangChain) = flexible, unopinionated — sab khud wire karo, poora control,
   par zyada code/setup. Kisi bhi tarah ka app bana sakte.
-- Next.js (LlamaIndex) = opinionated, batteries-included — conventions ready, kam code,
   ek kaam (RAG/data) jaldi ho jata, par framework ke tareeke me rehna padta.
-- kab React/LangChain: complex/custom flow, agents+tools+memory, poora control chahiye
-- kab Next.js/LlamaIndex: sidha RAG/PDF Q&A jaldi banana, data/index pe focus, kam code
-- dono galat/sahi nahi — kaam dekh ke chuno (achha dev dono jaanta)

**C2.** "Framework ne concepts chhupaye, mitaaye nahi" — LlamaIndex ki `.query()` line ke
example se yeh samjhao. (andar kya-kya ho raha hai)
**Mera jawab:**
-- engine.query(q) ek chhoti line, par andar poora RAG ho raha:
   1. query ko EMBED karo (Day 2)
   2. index me COSINE se top_k chunks RETRIEVE karo (Day 2+7)
   3. un chunks + query se PROMPT banao (Day 1)
   4. Claude ko bhejo aur JAWAB lo (Day 1)
-- yani sab concepts andar HAIN, bas dikhte nahi — framework ne WRAP kiya, delete nahi
-- humein pata hai andar kya hai kyunki humne scratch me khud banaya (scratch-first ki jeet)

---

## ✅ D. True / False (galat ho toh sahi karo)

**D1.** LlamaIndex LangChain se behtar framework hai, LangChain ab use nahi karna chahiye.
**Mera jawab:**
-- FALSE. Koi "behtar" nahi — dono alag kaam ke liye. LlamaIndex RAG/data pe specific,
   LangChain general (RAG+agents+tools). Kaunsa use karna = problem/zaroorat pe depend.
**D2.** LlamaIndex mukhya roop se data/RAG pe focused framework hai, jabki LangChain
general-purpose GenAI framework hai.
**Mera jawab:**
-- TRUE. LlamaIndex = RAG/data-focused; LangChain = general-purpose GenAI (RAG+agents+memory+tools).

### 🎯 Bonus (optional)
Tum ek naya project shuru kar rahe ho: (a) sirf ek "PDF Q&A bot" — jaldi banana hai; ya
(b) ek multi-agent system with tools, memory, RAG, aur custom routing. Har case mein
kaunsa framework chunoge aur kyun?
**Mera jawab:**
-- (a) sirf PDF Q&A bot, jaldi banana → LlamaIndex 🦙
   kyun: RAG/data-focused, kam code (from_documents + query_engine), fast setup.
   Simple kaam ke liye extra flexibility ki zaroorat nahi.
-- (b) multi-agent + tools + memory + RAG + custom routing → LangChain (+LangGraph)
   kyun: general GenAI framework — agents, tools, memory, custom flows sab support karta.
   LlamaIndex sirf RAG me strong, itna complex orchestration nahi.
-- (RAG part dono me plug ho sakta — par poore agentic system ke liye LangChain jeetta)
