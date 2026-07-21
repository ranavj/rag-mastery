# Day 8 — Exercise 📝

> **Rule:** Khud solve karo. Answers `**Mera jawab:**` ke aage likho. Notes dekhna allowed.
> Kal (Day 9 se pehle) submit karna.

---

## 🧮 A. Reasoning

**A1.** RAGBot mein `ingest()` aur `ask()` — inme se kaunsa SLOW hai aur kaunsa har baar
chalta hai? Design mein ingest ko "ek baar" kyun rakha (persist se skip)?
**Mera jawab:**
--- ingest(pdf) — load(D6)→clean(D6)→chunk(D3)→store(D5) — EK BAAR (persist se skip)
--- ask(query) — retrieve+threshold(D7)→Claude(D1)→answer+citation(D6) — HAR SAWAAL
-- SLOW: ingest (embedding calculation slow — Day 5 ka 69-ghante wala lesson)
-- HAR BAAR chalta: ask (per query)
-- ingest EK BAAR kyun: slow hai + result Chroma mein PERSIST ho jata ->
   dobara embed karne ki zaroorat nahi (count>0 to skip) -> app hamesha fast rehta
**A2.** `ask()` ek dict return karta hai: `{"answer": ..., "sources": [...]}`.
Sirf string (answer) return karne ke bajaye dict kyun better hai? (UI ke hisaab se socho)
**Mera jawab:**
-- sirf string hoti to bas answer milta, sources (page numbers) alag se nahi milte
-- dict {answer, sources} me UI ko dono cheezein ALAG-ALAG milti hain ->
   UI answer ko body me dikhata, sources ko neeche italic "📄 page [2,7]" style me
-- structured data = UI apni marzi se format/handle kar sakta (aage stars, links, wagera bhi add ho sakte)
-- frontend analogy: API JSON response {data, meta} jaisa — sirf raw string nahi

## 💻 B. Coding

**B1.** Streamlit script har interaction pe poora re-run hota hai. Agar hum `bot` ko
`st.session_state` mein NA rakhein, toh har sawaal pe kya bura hoga?
(React ke kis concept se yeh match karta hai?)
**Mera jawab:**
-- bina session_state: har sawaal pe script re-run -> bot dobara banega +
   messages=[] reset -> POORI CHAT HISTORY gayab (bot bhulakkad, pichla sawaal bhool jaye)
-- + bot re-init ka overhead har render pe (dobara Chroma connect)
-- React concept: useState — state jo re-render ke baad bhi BACHA rehta
   (st.session_state = Streamlit ka useState; bina iske sab local var, har render pe naye)
**B2.** RAGBot ki file mein CHUNK_SIZE, TOP_K, DISTANCE_THRESHOLD sab upar (top) ek jagah
rakhe hain. Yeh "config alag, code alag" pattern kyun accha hai?
**Mera jawab:**
-- DRY concept: ek jagah define, reuse anywhere
-- fayda: value change ek jagah -> har jagah apply (threshold 1.4->1.2 = ek line badlo)
-- readable/tune-able: file kholte hi TOP pe saare knobs dikh jate, poora code padhe bina
   (6 mahine baad aap ya team-mate turant samajh + tune kar sake)
-- frontend analogy: config.js / .env / constants file — settings alag, logic alag

## ✍️ C. Text / Short answer

**C1.** "Engine (rag_bot.py) UI (app.py) se alag" — yeh separation kyun important hai?
Frontend se ek example do (service vs component).
**Mera jawab:**
-- separation of concerns / MVC pattern — logic alag, UI alag
-- fayde:
   1. REUSABLE: ek engine, kai UI (aaj CLI + Streamlit dono ne use kiya, kal React)
   2. UI badlo logic safe: Streamlit -> React karo, rag_bot.py ek line na badle
   3. TESTABLE: engine ko UI ke bina test kar sakte (humne terminal se kiya tha)
-- example: Angular AuthService (logic) vs LoginComponent (UI) — component bas
   authService.login() bulata, login ka logic khud nahi jaanta.
   RAGBot = AuthService, app.py = LoginComponent
**C2.** Mentor ne BM25 (sparse) + dense (embeddings) hybrid dikhaya. Dono mein kya farak hai,
aur ek-ek example do jahan har ek jeetta hai.
**Mera jawab:**
-- dense (embeddings) = MEANING se match; BM25 (sparse) = exact SHABD/keyword se match
   (BM25 cache NAHI — yeh Day-1 keyword search jaisa, smart weighting ke saath)
-- BM25 jeeta: "BFL-PL-2024" (product code) — embeddings codes/numbers pe weak, BM25 exact match
-- dense jeeta: "installment nahi de paunga" — koi exact shabd nahi, par meaning se
   loan-default wala doc mil jata
-- isliye HYBRID (dono jodo, EnsembleRetriever) = codes bhi mile + meaning bhi (best of both)

## ✅ D. True / False (galat ho toh sahi karo)

**D1.** RAGBot ka `ask()` bina kisi guard ke har query pe LLM se jawab bana hi deta hai.
**Mera jawab:**
-- FALSE. Humara ask() mein threshold GUARD hai — agar koi chunk paas na ho to
   "jaankari nahi mili" return karta, LLM ko bulata hi nahi (pizza wala case).
   Isliye "bina guard ke banata hi hai" galat.
**D2.** Dense retrieval (embeddings) hamesha keyword/BM25 se behtar hota hai.
**Mera jawab:**
-- FALSE. Hybrid combination better — code/exact pe BM25, meaning pe dense.
   Dense hamesha behtar nahi (product code jaise cases me BM25 jeetta).

### 🎯 Bonus (optional)
Tumhara RAGBot abhi ek hi PDF pe kaam karta hai. Socho: agar 100 alag companies ki
policies daalni ho (multi-tenant), toh tum metadata + retrieval mein kya change karoge
taaki ek company ki query doosri company ke docs na chhue? (Day 5 filter yaad karo)
**Mera jawab:**
-- metadata me har chunk ke saath company_id daalo (jaise {"company_id": "acme", "source":..., "page":...})
-- retrieval me WHERE filter lagao: collection.query(..., where={"company_id": "acme"})
   -> search SIRF us company ke chunks me hota, doosri company ke docs chhu hi nahi sakte
-- Day 5 ka filter yahi tha (where={"category":"shipping"}) — ab multi-tenant security ke liye
-- (bonus: yeh security bhi hai — ek client ka data doosre ko kabhi na dikhe, data isolation)
