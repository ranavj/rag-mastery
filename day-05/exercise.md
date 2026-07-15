# Day 5 — Exercise 📝

> **Rule:** Khud solve karo. Answers `**Mera jawab:**` ke aage likho. Notes dekhna allowed.
> Kal (Day 6 se pehle) submit karna.

---

## 🧮 A. Reasoning

**A1.** Humara scratch store pehli baar chala toh 4 docs embed karne mein (maan lo) 2 second lage.
Dobara chalane pe load hone mein ~0 second. Ab socho 5 lakh docs hote:
pehli baar kitna time lagta (roughly, ratio se)? Aur dobara chalane pe kyun almost 0?
**Mera jawab:**
-- pehli baar: 4 docs ki EMBEDDING hui (text -> vector calculation) = 2 sec
-- ratio: 1 doc = 0.5 sec -> 5 lakh docs = 2,50,000 sec ≈ 69 GHANTE (~3 din nonstop!)
-- dobara: vectors disk pe stored hain -> koi calculation nahi -> ~0 sec
-- lesson: embedding LINEAR scale karti hai (docs 1.25 lakh guna = time bhi utna guna)
   isliye persistence convenience nahi, MAJBOORI hai
**A2.** Chroma ne query ka result diya: `doc A: dist=0.8` aur `doc B: dist=1.5`.
Kaunsa doc zyada relevant hai aur kyun? (dhyan: yeh distance hai, similarity nahi)
**Mera jawab:**
-- doc A (dist=0.8) zyada relevant hai — distance mein jitna KAM utna exact/similar
-- kyun: distance = do points ki DOORI. Kam doori = paas-paas = same meaning.
   (similarity ka ULTA khel: similarity mein zyada=better, distance mein kam=better)
-- sorting bhi ascending hogi (chhota distance pehle)

---

## 💻 B. Coding

**B1.** File 1 mein `save()` ke andar numpy vector ko `.tolist()` kyun karna pada?
(JS analogy: JSON.stringify kis cheez pe fail/weird hota hai?)
**Mera jawab:**
-- JSON sirf simple types jaanta hai (string, number, list, dict, bool)
-- numpy array ek SPECIAL object hai — json.dump() use samajh nahi pata -> TypeError (not serializable)
-- .tolist() = numpy array ko plain Python list banao -> ab JSON likh sakta hai
-- JS analogy: JSON.stringify(new Map()) = "{}" (gayab!), Date bhi weird —
   special objects ko pehle plain form mein convert karna padta = "serializable banana"
**B2.** `client.get_or_create_collection(name="policies")` — is method ke naam mein hi
persistence ka raaz chhupa hai. "get_or_create" ka matlab kya, aur yeh dobara-run pe
kya karta hai?
**Mera jawab:**
-- get_or_create = pehli baar CREATE karo, agli baar GET karo (wahi existing kholo)
-- dobara-run pe: naya nahi banata — disk se purana collection uthata, SAARE stored
   docs + embeddings ke saath (isliye collection.count() == 5 mila, re-embed nahi hua)
-- yeh File 1 ke `if not store.load():` wale pattern ka built-in version hai (persistence!)

---

## ✍️ C. Text / Short answer

**C1.** Kal wali script `day-05/` folder ke andar se chalane pe `FileNotFoundError` kyun aaya tha,
aur `os.path.dirname(__file__)` ne use kaise fix kiya? (apne shabdon mein)
**Mera jawab:**
-- code mein path tha "day-05/my_store.json" (RELATIVE path)
-- relative path wahan se resolve hota jahan se script RUN karte ho, script ki jagah se nahi
-- maine day-05/ ke ANDAR se chalaya -> usne dhundha day-05/day-05/my_store.json -> aisa
   folder hi nahi -> FileNotFoundError
-- fix: os.path.dirname(__file__) = "script khud jahan hai woh folder" -> path SCRIPT se
   bandh gaya -> ab kahin se bhi chalao, hamesha sahi jagah file milegi
-- JS analogy: relative <img src> current page se resolve hota; Node ka __dirname = yahi cheez

**C2.** Metadata filter (`where={"category": "shipping"}`) ne "din" wala retrieval bug kaise fix
kiya? Ek real app ka example do jahan aap yeh filter use karoge.
**Mera jawab:**
-- query "saamaan kitne din mein aayega?" pe weak model "din" shabd se confuse hoke
   Refund doc ko #1 rank de raha tha (galat category ka doc)
-- where={"category": "shipping"} lagaya -> search SIRF shipping docs ke andar hua ->
   Refund doc race mein tha hi nahi -> sahi doc (Express delivery) #1 aa gaya
-- lesson: filter galat candidates ko pehle hi bahar kar deta -> weak model bhi galti nahi kar pata
-- real app example: e-commerce support bot — user "Orders" page pe hai toh
   where={"category": "orders"}; ya multi-client docs app mein where={"client_id": "X"}
   (taaki ek client ko doosre ka data kabhi na dikhe — security + relevance dono)

---

## ✅ D. True / False (galat ho toh sahi karo)

**D1.** Chroma mein `metadatas={"source": "policy.pdf"}` likhne se Chroma policy.pdf file
ko khol ke padh leta hai.
**Mera jawab:**
-- FALSE. Metadata sirf ek LABEL/tag hai (HTML data- attribute jaisa) — Chroma koi file
   nahi kholta. Humne jo string likhi, woh bas store hui. Asli PDF loading = Day 6 (loaders).
**D2.** ChromaDB ko documents dene se pehle humein khud `model.encode()` se embed karna
zaroori hai.
**Mera jawab:**
-- FALSE. Chroma khud embed karta hai — bas text do (query bhi text mein).
   Uska apna default model hai (wahi all-MiniLM — 79MB download hua tha).
   Chaaho toh apna embedding function de sakte ho (sir ne OpenAIEmbeddings diya tha).
---

### 🎯 Bonus (optional)
Mentor ne session-05 mein **Pinecone** (cloud vector DB) use kiya, humne **Chroma** (local).
Ek situation batao jahan Chroma better choice hai, aur ek jahan Pinecone.
(hint: localStorage vs Firebase kab use karte ho?)
**Mera jawab:**
-- CHROMA (local) better jab: learning/prototype/personal project, chhota data,
   sab kuch apne laptop/server pe, free chahiye, internet dependency nahi
   (= localStorage: chhota, free, local, setup zero)
-- PINECONE (cloud) better jab: production app, crores of vectors, multiple
   users/servers ek hi DB access karein, scaling/backup managed chahiye
   (= Firebase: managed, scalable, team-shared — par paid + internet zaroori)
-- humara roadmap: seekhne ke liye Chroma perfect; Phase 5 project mein bhi Chroma
   se shuru, zaroorat padi toh cloud pe shift (interface similar hi rehta)
