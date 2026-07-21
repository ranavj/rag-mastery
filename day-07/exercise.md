# Day 7 — Exercise 📝

> **Rule:** Khud solve karo. Answers `**Mera jawab:**` ke aage likho. Notes dekhna allowed.
> Kal (Day 8 se pehle) submit karna.

---

## 🧮 A. Reasoning

**A1.** MMR retriever mein `k=3, fetch_k=3` set hai. MMR ko diversity dene ke liye
kitne candidates milte hain, aur usme se kitne chunne hain? Diversity aayegi ya nahi — kyun?
**Mera jawab:**
-- candidates: fetch_k=3 -> sirf 3 candidates milte hain (pool chhota)
-- chunne hain: k=3 -> teeno lene hi hain
-- diversity NAHI aayegi -> 3 aaye, 3 hi lene hain, MMR ke paas koi CHOICE nahi
   (variety kahan se laaye jab sabko lena hi hai)
-- fix: fetch_k >> k (jaise fetch_k=10, k=3) -> bade pool mein se best+alag chun sake
**A2.** Ek query ka jawab document mein hai hi nahi. Bina threshold ke retriever kya karega,
aur user ko iska kya nuksaan (LLM ke context mein)?
**Mera jawab:**
-- bina threshold: Chroma kuch na kuch de hi dega (top-3, chahe bahut door/irrelevant ho)
   (pizza query pe Gold-appraisal jaisa kachra aaya tha)
-- nuksaan: yeh kachra chunks CONTEXT ban ke Claude ko jaate hain -> Claude us faltu
   context se ek confident-sa (par galat) jawab bana sakta = HALLUCINATION risk
   + faltu tokens waste
-- threshold LAGANE se: door wale reject -> "jawab nahi mila" bolta -> hallucination se BACHTA
   (yani threshold = anti-hallucination guard)

## 💻 B. Coding

**B1.** Humare scratch MMR mein `lam=0.5` pe results nahi badle, `lam=0.1` pe badle.
Iska asli technical reason kya tha? (do metrics ka naam lo)
**Mera jawab:**
-- do metrics alag SCALE pe the:
   1. relevance = -distance -> range chhota (-1.1 se -1.3, farak ~0.2)
   2. repeat = cosine -> range bada (0 se 1, farak ~0.7)
-- bina normalize kiye jodne se lam=0.5 pe koi meaningful farak nahi bana -> ranking wahi rahi
-- lam=0.1 ne diversity ko itna zyada weight diya ki chhota farak bhi dikhne laga -> results badle
-- fix: do alag metrics jodne se PEHLE dono ko same scale (0-1) pe normalize karo

**B2.** `search_type="similarity_score_threshold"` mein hum `score_threshold=0.25` dete hain.
Yahan ZYADA score better hai ya KAM? Aur Chroma ke raw `distances` mein ZYADA better tha ya KAM?
(dono ka farak batao)
**Mera jawab:**
-- similarity_score_threshold mein: ZYADA score = better (similarity, 0-1 range)
   -> 0.25 se UPAR wale rakho, neeche wale reject
-- Chroma ke raw distances mein: KAM = better (distance = doori)
   -> chhoti distance = zyada similar
-- dono ULTE hain: similarity zyada=achha, distance kam=achha (same "paas hona", ulti disha)
-- isliye threshold hamesha ASLI scores dekh ke tune karo (galti se ulta lagao to
   sahi results reject ho jate — mera 0.3 ne EMI query @0.297 ko reject kar diya tha)

---

## ✍️ C. Text / Short answer

**C1.** MMR ko apne shabdon mein samjhao — ek real-life ya real-product example do
(daal-thali ke alawa apna socho).
**Mera jawab:**
-- MMR ek way hai variety add karne ka — results relevant BHI hon aur aapas mein ALAG bhi
   (sirf best-best-best nahi, warna wahi baat repeat aati)
-- lambda knob se decide hota kitni relevance vs kitni diversity
-- real example: YouTube/Spotify — ek video/gaana dekha to same cheez ki 10 copies nahi,
   milte-julte PAR alag suggestions aate

**C2.** Mentor ke BFL_chatbot config mein 2 galtiyan thi. Dono batao aur har ek ka asar.
**Mera jawab:**
-- config: {'k':3, 'fetch_k':3, 'lambda_mult':0.7, 'threshold':0.9}
-- Galti 1: k aur fetch_k dono 3 (fetch_k == k) -> MMR ke paas choose karne ko candidates
   nahi -> variety limited/zero (MMR laga ke bhi normal search jaisa)
-- Galti 2: 'threshold':0.9 sirf similarity_score_threshold mode mein chalta, yahan
   search_type='mmr' hai -> threshold SILENTLY ignore -> kachra reject nahi hota

## ✅ D. True / False (galat ho toh sahi karo)

**D1.** `fetch_k` hamesha `k` ke barabar hona chahiye.
**Mera jawab:**
-- False fetch_k zayada hona chahiye tabhi MMR apna impact daal skta
**D2.** Threshold lagane se system "jawab nahi mila" bol sakta hai, jo hallucination se bachata hai.
**Mera jawab:**
--- True bina Threshold chorma DB kuch na kuch galt jabab add kar dega

### 🎯 Bonus (optional)
Tum ek support-bot bana rahe ho jahan users kabhi-kabhi aise sawaal poochte hain jo
docs mein hain hi nahi. Teeno knobs (top_k, threshold, MMR) mein se kaunsa sabse zaroori
hai aur kyun? Apne project ke hisaab se justify karo.
**Mera jawab:**
-- THRESHOLD sabse zaroori is case mein
-- kyun: users aise sawaal poochte jo docs mein hain hi nahi. Bina threshold ke bot
   har baar "kuch to" jawab bana dega (galat/hallucinated) -> user ka trust tootega
-- threshold se bot "yeh mujhe nahi pata, support se poochho" bol sakta -> safe + honest
-- (top_k aur MMR quality/variety improve karte, par GALAT jawab dene se rokna =
   threshold ka kaam, jo support-bot ke liye sabse critical hai)
