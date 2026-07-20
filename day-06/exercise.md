# Day 6 — Exercise 📝

> **Rule:** Khud solve karo. Answers `**Mera jawab:**` ke aage likho. Notes dekhna allowed.
> Kal (Day 7 se pehle) submit karna.

---

## 🧮 A. Reasoning

**A1.** Humari PDF ke 12 pages se 40 chunks bane (chunk_size=500, overlap=80).
Total text ~17,000 chars tha (cleaning ke baad). Step formula se check karo —
kya ~40 chunks banna sahi lagta hai? (step = chunk_size - overlap, phir 17000 ÷ step)
**Mera jawab:**
-- step = chunk_size - overlap = 500 - 80 = 420  (har chunk 420 NAYE chars cover karta)
-- chunks ≈ total ÷ step = 17,000 ÷ 420 ≈ 40.5 → ~40
-- code se mile the EXACTLY 40 → formula ka prediction sahi! 
**A2.** Agar hum CLEAN step skip kar dete, toh wahi query ("EMI bounce penalty") pe
kya farak aata? (2 problem batao — Day 3 ke "grey vector" lesson se jodo)
**Mera jawab:**
-- Problem 1: har chunk mein same boilerplate ("BAJAJ FINANCE... CONFIDENTIAL...") ghusa rehta
   -> har vector mein same MILAWAT -> vectors blurry/grey (Day 3 lesson)
   -> sab chunks FARZI-SIMILAR ho jate -> scores milte-julte, retrieval farak nahi kar pata
-- Problem 2: chunk space + TOKEN WASTE -> 500 chars mein ~40% kachra, asli content kam;
   retrieved chunk ke saath wahi kachra Claude ko bhi jata (paisa + noise)
-- (bonus: same boilerplate baar-baar embed karna = repeated embedding = compute waste)

---

## 💻 B. Coding

**B1.** `loader.load()` kya return karta hai — plain strings ya kuch aur?
Us object ke 2 hisse kaunse hain aur har ek mein kya hota hai?
**Mera jawab:**
-- plain strings NAHI — "Document" objects ki list deta hai (har page = ek Document)
-- 2 hisse, text aur metadata saath-saath:
   1. doc.page_content = asli TEXT (page ka content)
   2. doc.metadata = extra info dict — source (file path), page number, total_pages, author...
-- isi wajah se aage chunks ko bhi apna source/page pata rehta (virasat)

**B2.** Day 3 mein humne `split_text()` use kiya tha, aaj `split_documents()`.
In dono mein kya farak hai, aur aaj wala kyun better tha?
**Mera jawab:**
-- split_text: sirf TEXT ke tukde deta tha (plain strings) — source/page ka pata kho jata
-- split_documents: text ke saath METADATA bhi deta hai — har chunk apne page ka
   metadata VIRASAT mein leta (source, page number)
-- kyun better: isi se search result mein PAGE CITATION mila ("jawab page 2 se") —
   bina iske pata hi nahi chalta kaunsa chunk kahan se aaya

---

## ✍️ C. Text / Short answer

**C1.** Apne shabdon mein: "loader" kya hai? Frontend ki kisi cheez se compare karo.
**Mera jawab:**
-- loader = parser/adapter jo kisi bhi format (PDF/CSV/web) ko KHOL ke
   plain text + metadata deta hai (Document object)
-- chunks NAHI banata — woh splitter ka kaam (loader KHOLTA hai, splitter TODTA hai)
-- frontend compare: JSON.parse() jaisa — raw string -> usable object;
   ya API adapter layer — alag-alag sources (JSON/XML/CSV), ek common format,
   aage ka code (components) same rehta

**C2.** "Citations" (jawab ke saath source/page dikhana) user ke liye kyun important hai?
Yeh humare pipeline mein kis cheez se possible hua?
**Mera jawab:**
-- kyun important: retrieved chunk ke metadata se bata sakte "jawab policy.pdf ke PAGE 2
   se aaya" -> user khud VERIFY kar sakta = TRUST. AI pe andha bharosa nahi karna padta.
   (Perplexity/Claude ke [source] wale answers isi pe bane hain)
-- kis cheez se possible: LOADER ne har page ko real metadata diya (source+page),
   aur split_documents ne har chunk ko woh metadata VIRASAT mein diya ->
   search result ke saath metadata wapas mila -> citation ready

---

## ✅ D. True / False (galat ho toh sahi karo)

**D1.** PDF file ko `open()` + `f.read()` se seedha padh ke text mil jata hai.
**Mera jawab:**
-- FALSE. PDF binary format hai — f.read() se internal structure/kachra milta
   (%PDF-1.4, /BaseFont... — terminal pe khud dekha). Text compressed streams mein hota.
   Sahi: PARSER chahiye (pypdf / PyPDFLoader) jo decode karke text de.
**D2.** `split_documents()` ke baad har chunk apne source page ka metadata saath rakhta hai.
**Mera jawab:**
-- TRUE. Metadata virasat — isi se page citations bane.
---

### 🎯 Bonus (optional)
Mentor ne CSVLoader bhi dikhaya (customers.csv — rows ko text banaya).
Socho: ek CSV row `['BF003', 'Rajan Mehta', 'Home', '22000', 'Default']` text ban ke
Chroma mein gayi. Ek sawaal likho jo semantic search se is row ko dhundh le
(bina exact words use kiye) — aur batao metadata mein kya rakhna smart hoga.
**Mera jawab:**
-- chalaak sawaal (exact words nahi): "Kaunse customers ne apni EMI nahi bhari?"
   ya "ghar ke loan pe kaun paise nahi de raha?"
   -> "Default" shabd use nahi kiya, par semantic search samjhega
   (EMI nahi bhari / paise nahi de raha ≈ Default status; ghar ka loan ≈ Home)
-- metadata mein smart: {"customer_id": "BF003", "loan_type": "Home", "status": "Default",
   "emi": 22000, "source": "customers.csv", "row": 3}
-- kyun: phir WHERE filter lag sakta — where={"status": "Default"} ->
   sirf defaulters mein search (Day 5 wala filter hathiyar, structured data pe!)
-- lesson: CSV jaisa STRUCTURED data ho toh key fields ko metadata mein bhi rakho —
   semantic search (meaning) + filter (exact) DONO ki taakat milti hai
