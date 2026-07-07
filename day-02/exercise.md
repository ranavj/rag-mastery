# Day 2 — Exercise 📝

> **Rule:** Yeh khud solve karo. Answers agle din (Day 3 shuru hone se pehle) Claude ko submit karo.
> Jhaank-jhaank ke notes dekhna allowed hai (yeh seekhne ke liye hai, exam nahi 🙂).
> Apne jawab neeche `**Mera jawab:**` ke aage likhte jao.

---

## 🧮 A. Calculation (cosine math)

**A1.** Do vectors hain `a = [3, 4]` aur `b = [3, 4]`.
Inka cosine similarity score kya hoga? (hint: same vector hai)
**Mera jawab:** 1 hoga answer
--dot product
rule jodi-jodi guna karke jodo
loop 1 = ai = 3, bi = 3
loop 2 = ai = 4, bi = 4
loop 1 total = (3*3) = 9
loop 2 total =  9 + (4*4) = 25
-- magnitude 
magnitude of a 
v1= [3,4]
x*x = 3* 3 = 9
y*y = 4*4 = 16
sum of v1 = 9 + 16 = 25 and square root is  5 
same mangnitude of b result 5 
-- final score
rule = dot / (magA * magB)
score = 25 / (5 * 5) = 25 / 25 = 1
-- kyun 1? sab ka jod / (magnitude1 * magnitude2)
dono vector bilkul same hai -> same direction -> angle 0 -> cosine(0) = 1
**A2.** Vectors `a = [2, 0]` aur `b = [0, 5]`.
Pehle inka **dot product** nikalo, phir bina poora formula kiye batao final score kya hoga aur kyun.
**Mera jawab:** score = 0 hoga

-- dot product (do vectors ke beech, jodi-jodi guna karke jodo)
loop 1 = a1 = 2, b1 = 0 -> 2*0 = 0
loop 2 = a1 = 0, b1 = 5 -> 0*5 = 0
dot product = 0 + 0 = 0

-- magnitude (har vector ki apni size: square karo, jodo, square root)
mag(a) = [2,0] -> 2*2 + 0*0 = 4  -> square root of 4  = 2
mag(b) = [0,5] -> 0*0 + 5*5 = 25 -> square root of 25 = 5

-- final score (rule: dot / (magA * magB))
score = 0 ÷ (2*5) = 0 ÷ 10 = 0

-- kyun 0?
dot product hi 0 aa gaya -> upar 0 hai toh poora score 0.
Vectors 90 degree alag hain (ek X-direction, ek Y-direction) -> cosine(90) = 0 -> bilkul alag.
---

## 💻 B. Coding

**B1.** `01_cosine_scratch.py` ke `magnitude()` function ko dekhe bina,
vector `[6, 8]` ki magnitude (size) kya hogi? (Pythagoras lagao, answer ek pura number aayega)
**Mera jawab:**
-- magnitude har vector ki apni size square karo , jodo, square root
mag(a) = [6, 8] -> 6*6 + 8*8 = 100 -> square root of 100 is 10
**B2.** `02_semantic_rag.py` mein `retrieve()` ko agar `top_k=3` ke saath bulao,
toh Claude ko kitne documents jayenge? Aur zyada top_k ka ek fayda + ek nuksaan likho.
**Mera jawab:**
agar top_k = 3 hai iska matlab jinka consine score top par hai query ke saath voh 3 doc jayenge
-- fayda: sahi doc miss hone ke chances kam (safety net - ek galat ho to doosra bacha le)
-- nuksan 1: token consumption zayada -> paisa zayada + slow
-- nuksan 2: bahut zyada top_k -> faltu/unrelated docs bhi chale jate -> LLM confuse (noise)
-- balance: na bahut kam (sahi doc chhoot jaye) na bahut zyada (noise). sweet spot ~3 se 5
---

## ✍️ C. Text / Short answer

**C1.** Apne shabdon mein (2-3 line): "keyword search" aur "semantic search" mein kya farak hai?
Ek example do jahan keyword fail karega par semantic pass.
**Mera jawab:**
-- keyword search: jaise FE mein search bar par result search karte -> DB se data aata SAME search words ke base par (bas shabd match)
-- semantic search: sirf keywords par nahi, uska meaning/sense bhi analyze karti hai

keyword 2 tarah se fail hota hai, semantic dono jagah pass:
-- flavor 1 (synonyms - alag shabd same meaning): "refund" vs "paisa wapas"
   keyword MISS kar deta (koi common shabd nahi), semantic pakad leta
-- flavor 2 (polysemy - same shabd alag meaning): "bank of river" vs "money in bank"
   keyword GALAT match karta (bas "bank" shabd dekh ke), semantic sense se alag kar deta
**C2.** File 2 chalane par Refund doc top pe kyun nahi aaya? (jo lesson humne dekha)
**Mera jawab:**
-- dono docs (Support aur Refund) mein "din" shabd tha, sirf Refund mein nahi tha - yeh galat soch thi
-- asli reason: model weak hai (Hinglish theek se nahi samajhta)
-- use "paisa wapas = refund" ka MEANING samajh nahi aaya
-- isliye surface shabdo par score kar diya, aur Support ko galti se Refund se upar rakha (0.456 vs 0.371)
-- lesson: weak model meaning ke bajaye surface (upar-upar ke shabd) par atak jata hai
---

## ✅ D. True / False (sahi/galat — aur galat ho toh sahi karo)

**D1.** Cosine similarity ka score hamesha 0 aur 1 ke beech hota hai, aur 1 = bahut similar.
**Mera jawab:**
-- true
**D2.** Embedding model jitna bada/achha ho, semantic search ki quality utni hi achhi — model choice se koi farak nahi padta.
**Mera jawab:**
-- false
---

### 🎯 Bonus (optional)
`KNOWLEDGE_BASE` mein apni 2 nayi lines add karo (jaise "Cancellation policy: ...")
aur ek aisa sawaal socho jiska sahi jawab tabhi aaye jab semantic search kaam kare.
**Mera jawab:**

-- 2 nayi lines KNOWLEDGE_BASE mein:
"Cancellation policy: Order ship hone se pehle kabhi bhi cancel kar sakte hain.",
"EMI: 10000 se upar ke order par 3 mahine ki no-cost EMI available.",

-- chalaak sawaal (doc wale exact shabd nahi, synonym use kiya):
Sawaal: "Kya main apna order wapas le sakta hun?"

-- kyun yeh semantic ko test karta hai:
sawaal mein "cancel" shabd nahi hai ("order wapas lena" bola).
keyword search FAIL karega (koi common shabd nahi).
semantic search PASS karega (meaning samajh jayega = cancellation policy).

-- bonus test case 2:
Sawaal: "Mahange saaman ko kishton mein le sakta hun?"
"EMI" ya "kishton" ka exact match nahi -> keyword fail, semantic pakad lega (EMI = kishton).
