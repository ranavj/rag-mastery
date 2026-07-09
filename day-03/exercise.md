# Day 3 — Exercise 📝

> **Rule:** Khud solve karo. Answers `**Mera jawab:**` ke aage likho. Notes dekhna allowed.
> Kal (Day 4 se pehle) submit karna.

---

## 🧮 A. Calculation (chunking math)

**A1.** Text 100 characters ka hai. `chunk_size = 40`, `overlap = 10`.
Har chunk ke start positions kya honge? (0, ?, ?, ...) — aur kitne chunks banenge?
(hint: step = chunk_size - overlap)
**Mera jawab:**
-- text 100 characters ka
-- step = chunk_size - overlap = 40 - 10 = 30
-- start positions: 0, 30, 60, 90
   Chunk 1: 0 -> 40
   Chunk 2: 30 -> 70
   Chunk 3: 60 -> 100
   Chunk 4: 90 -> 100 (sirf 10 chars bache, text khatam -> last chunk chhota)
-- total 4 chunks honge

**A2.** `chunk_size = 50`, `overlap = 50` rakh diya (galti se dono barabar).
Kya hoga? (step ki value nikalo aur socho loop ka kya haal hoga)
**Mera jawab:**
-- step = chunk_size - overlap = 50 - 50 = 0
-- start += 0 -> start kabhi aage nahi badhta -> hamesha 0 pe atka
-- while start < len(text) hamesha True -> INFINITE LOOP
-- same chunk (text[0:50]) baar-baar list mein add hota rahega -> RAM bhar jayegi -> MemoryError / hang
-- (stack overflow NAHI, kyunki recursion nahi hai — yeh while loop hai)
-- lesson: overlap hamesha chunk_size se KAM hona chahiye, warna step <= 0
---

## 💻 B. Coding

**B1.** `01_chunking_scratch.py` ke `chunk_text()` function mein `step` ki line hai:
`step = chunk_size - overlap`. Agar overlap `chunk_size` se BADA kar do (jaise size=30, overlap=40),
toh step positive rahega ya negative? Aur code ka kya behaviour hoga?
**Mera jawab:**
-- step = chunk_size - overlap = 30 - 40 = -10 (NEGATIVE)
-- start += -10 -> start negative hota jayega: 0, -10, -20, -30...
-- Python string slicing ERROR nahi deta (galat/negative index pe bhi chalta hai,
   negative index = end se ginti; ulta slice jaise text[45:20] = khali string "")
-- while start < len(text) hamesha True (start negative) -> INFINITE LOOP
-- garbage/khali chunks bante rahenge -> RAM bhar -> MemoryError / hang
-- (JS hota to shayad undefined deta, par Python chupchaap galat kaam karta rehta - no error)
-- lesson: overlap hamesha chunk_size se KAM ho (step > 0), warna infinite loop

**B2.** Scratch chunking "RAG" jaise words ko beech se tod deti thi. Library
(`RecursiveCharacterTextSplitter`) yeh kaise avoid karti hai? (separators list ka role batao)
**Mera jawab:**
-- library ke paas separators ki PRIORITY LIST hai: ["\n\n", "\n", " ", ""]
-- pehle paragraph (\n\n) pe todne ki koshish, na ho to line (\n) pe,
   na ho to space ( ) pe <- yahan word poora rehta hai, last resort character pe
-- "recursive" = upar se neeche try karta jab tak chunk fit na ho
-- KYUN words nahi tootte: space pe cut hamesha DO words ke BEECH lagta hai,
   word ke andar nahi. Scratch character gin ke kaatta tha (aankh band), isliye words tootte the.
**Mera jawab:**

---

## ✍️ C. Text / Short answer

**C1.** Apne shabdon mein: overlap kyun zaroori hai? Ek example do jahan overlap na hone se
meaning tut jaye.
**Mera jawab:**
-- overlap isliye important hai kyunki jab paragraph ki chunking hoti hai,
   tab har chunk apne aap mein poori baat nahi bol pata
-- overlap pichhle chunk ka thoda context saath le aata hai -> meaning bachi rehti

-- BINA overlap (meaning tut-ti):
   Chunk 1: "...hoti hai. Ye"       <- "Yeh" beech se kata
   Chunk 2: "h leave delivery..."   <- "h leave" = kaunsi leave? context gaya

-- overlap KE SAATH (fix):
   Chunk 2: "hoti hai. Yeh leave delivery se pehle..."  <- context bacha
**C2.** Chunk size bahut BADA (jaise poori book = 1 chunk) rakhne se kya 2 problem aati hain?
(retrieval quality ke hisaab se socho, sirf speed nahi)
**Mera jawab:**
-- Problem 1 (LLM/answer stage): ek bade chunk mein bahut alag topics ghuse hote
   eg: leave policy, events, salary breakup, etc
   user sirf leave pooche par events/salary sab bhi LLM ko jaata
   -> noise, LLM confuse, time-taking, token consumption zyada
-- Problem 2 (retrieval stage): bade chunk ka embedding "grey/blurry" ban jata
   (sab topics ka average) -> kisi bhi specific query se theek se match NAHI karta
   -> retrieval khud kamzor. Chhote focused chunks ka vector ek topic pe sharp hota hai.
---

## ✅ D. True / False (galat ho toh sahi karo)

**D1.** Library chunking mein har chunk hamesha bilkul `chunk_size` ke barabar hota hai.
**Mera jawab:**
-- false
**D2.** Overlap ka matlab hai — do chunks ka kuch hissa common/repeat hota hai.
**Mera jawab:**
-- yes
---

### 🎯 Bonus (optional)
Apni koi 3-4 line ki text socho, aur haath se (bina code) `chunk_size=20, overlap=5` se
chunks bana ke likho. Phir batao kaunse words boundary pe tut sakte hain.
**Mera jawab:**
-- text: "React se hum UI banate hain jaldi aur easily"  (44 chars)
-- step = chunk_size - overlap = 20 - 5 = 15
-- start positions: 0, 15, 30

Chunk 1: text[0:20]  = "React se hum UI bana"      <- "banate" beech se kata
Chunk 2: text[15:35] = " banate hain jaldi a"      <- "aur" beech se kata ("a" par)
Chunk 3: text[30:45] = "ldi aur easily"            <- "jaldi" beech se kata ("ldi")

-- overlap dikhta hai: Chunk 1 end "...bana", Chunk 2 start " bana..." (5 char repeat)
-- boundary pe tut-ne wale words: banate, aur, jaldi
-- (character-based scratch isliye words tootte; library space pe kaat ke bachati)
