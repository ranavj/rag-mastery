# Day 17-18 — Exercise 📝

> **Rule:** Khud solve karo. Answers `**Mera jawab:**` ke aage likho. Notes dekhna allowed.
> Next session se pehle submit karna.

---

## 🧮 A. Calculation / Reasoning

**A1.** Scratch loop me `max_steps=4`. Ek query jo pehle `policy_search`, phir
`account_balance` chalati hai aur uske baad final jawab deti hai — woh **kitni LLM
API calls** karegi? (Sochna: har step me ek LLM call. Tool khud chalne me LLM call
hoti hai kya?)
**Mera jawab:**
--- Total = 3 LLM API calls.
    step 1 -> LLM sochta -> policy_search chuni      (call #1)
    step 2 -> LLM result dekhta -> account_balance   (call #2)
    step 3 -> LLM dono result se final ANSWER        (call #3)
--- max_steps=4 = MAXIMUM cap (safety-net, infinite loop se bachne ko), fixed count nahi.
    Yahan 3 me jawab mil gaya -> loop sirf 3 baar chala, 4th iteration aaya hi nahi
    (ANSWER milte hi return).
--- Tool KHUD chalna (cosine search / dict lookup) = plain Python, usme LLM call NAHI.
    LLM call sirf 2 jagah: tool chunne se PEHLE (soch) + result aane ke BAAD (agla kadam).
    Yaani per step = 1 LLM call (LLM ki soch), tool ka run us call ka hissa nahi/free.
**A2.** `policy_search` me `np.argsort(scores)[::-1][:2]`. Agar
`scores = [0.31, 0.88, 0.55]` ho, to function **kaunse do docs (index)** laut'ega
aur **kis order me**? (argsort ascending deta hai — dhyaan se.)
**Mera jawab:**
--- Jawab: index [1, 2] (order: index 1 pehle, phir index 2 = bade score pehle).
    scores = [0.31, 0.88, 0.55]  ->  index =  0     1     2
    step1 argsort (chhote->bade INDEX) = [0, 2, 1]   (0.31=idx0, 0.55=idx2, 0.88=idx1)
    step2 [::-1] ulta (bade->chhote)   = [1, 2, 0]
    step3 [:2] top-2                    = [1, 2]   -> doc-1 (0.88) top, doc-2 (0.55) doosra
--- DHYAAN: argsort VALUES nahi, INDEX (position) lautata hai. Isliye jawab 0.88/0.55
    (values) nahi, [1, 2] (un values ki position). doc-0 (0.31, sabse kam) chhoot gaya.
## 💻 B. Coding

**B1.** Scratch agent (`01_...`) me ek **teesra tool** `emi_calculator` add karo.
Uska Python function likhne ki zaroorat nahi — sirf `TOOLS` dict me entry (naam +
**description with LIMIT**) likho, aur **ek query** batao jispe agent ise chunega
(aur `policy_search`/`account_balance` ko nahi).
**Mera jawab:**
--- TOOLS dict entry (description = MANUAL: role + input + LIMIT, na ki example queries):
    "emi_calculator": (
        emi_calculator,
        "Diye gaye principal, interest rate aur months se EMI (monthly "
        "installment) calculate karta hai. Input = principal, rate, months. "
        "Policy charges ya account balance ke sawaal ke liye NAHI.",
    ),
--- Query jispe agent ise chunega: "6 hazar ka loan, 10% rate, 6 months — EMI kitni?"
    (ya "iPhone17 ki 6 months EMI batao" — routing emi_calculator pe hi, bas agent
     principal/rate wapas poochega kyunki wo numbers query me nahi the.)
--- GALTI jo pakdi: pehle maine description ki jagah example SAWAAL likh diye the.
    Description = tool KYA KARTA + input + kab NAHI (lakshman rekha), example queries nahi.
**B2.** Library file (`02_...`) me `AgentExecutor(agent=agent, tools=TOOLS,
verbose=True)` ke saath `max_iterations=1` set kar do. Ab **combined query**
("VJ-100 ki EMI bounce charge + balance", jise 3 steps chahiye) chalane par kya
farak aayega? Code change (1 line) + expected behaviour likho.
**Mera jawab:**
--- Code change (1 line): AgentExecutor(agent=agent, tools=TOOLS, verbose=True, max_iterations=1)
--- Behaviour: combined query ko 3 steps chahiye (policy_search -> account_balance -> answer),
    par max_iterations=1 se agent ko sirf 1 turn milta hai:
      * agent SIRF pehla tool chala paayega (maano policy_search = charge).
      * doosra tool (account_balance = balance) chalane ka mauka nahi -> limit khatam.
      * jawab ADHURA: ya sirf ek hissa (charge YA balance), ya LangChain ka default
        "Agent stopped due to iteration limit" (early_stopping_method='force' default).
--- Yeh wahi max_steps CAP hai (A1 wala), bas itna chhota (1) ki 3-step query poori ho hi nahi
    sakti. Sabak: cap agent ko infinite loop se bachata, par bahut chhota = kaam adhura.
## ✍️ C. Text / Short answer

**C1.** Apne shabdon me: agent ka **self-correcting** hona kya hota hai? Aaj ki
file se (ya naya) ek example do jahan tool ka result **bura/khaali** aaya aur agent
ne apna jawab uske hisaab se badla.
**Mera jawab:**
--- Definition: self-correcting = agent tool ka RESULT dekh kar apna agla kadam / jawab
    badal leta hai — result bura/khaali ho to ruk jaata ya sach bol deta, ek fixed
    script ki tarah aankh band karke aage nahi badhta.
--- Example: query "VJ-999 ka balance" (account hai hi nahi) -> account_balance tool ne
    "Account 'VJ-999' nahi mila" lautaaya -> agent ne fake balance NAHI banaya, seedha
    user ko sach bataya. Result bura tha, isliye agent ne apna jawab uske hisaab se badla.
--- Connect: Day 8 threshold guard + Day 12 faithfulness wali anti-hallucination, ab agent
    ke andar (grounding banae rakha).
**C2.** "Description = tool ki lakshman rekha." (a) **under-scoped** (bahut narrow)
description ka nuksan, aur (b) **jhoothi/colliding** description ka asar — dono alag
likho. Aaj ke do live experiment yaad karo (kaun reliable failure tha, kaun me
Claude bach gaya aur kyun).
**Mera jawab:**
--- (a) UNDER-SCOPED (bahut narrow) ka NUKSAN = Try B (reliable failure): policy_search desc
    ko sikoda "sirf foreclosure, EMI bounce NAHI". EMI query pe agent ne tool CHALAYA HI NAHI
    (Invoking line gayab) -> apni yaaddasht se jawab = HALLUCINATION (grounding toota, Day 12).
    Data doc me tha phir bhi RAG na chala -> tool bhookha reh gaya.
--- (b) JHOOTHI/COLLIDING ka ASAR = Try A: balance tool ko bola "main policy ka hoon". Do baar
    try -> Claude ne DONO baar SAHI tool chuna (bach gaya). Kyun? tool ka NAAM + SAARE tools ki
    desc ek saath cross-check hote -> ek jhoothi line fool nahi karti (modern tool-calling robust).
--- Nichod: under-scope = reliable failure (khatarnaak); jhoothi = aksar bach jaata par reliability
    girti. Isliye "kharab desc = pakka galat" GALAT dawa hai.
## ✅ D. True / False (galat ho toh sahi karo)

**D1.** LLM khud apne computer par Python function chala deta hai, isliye humein
raw string ko parse karne ki zaroorat nahi hoti.
**Mera jawab:**
--- FALSE. LLM khud function nahi chalata — woh bas RAW STRING deta hai ("policy_search chalao").
    Hum us string ko PARSE karke (regex / native tool-call) sahi Python function KHUD chalate hain.
    Isliye parsing zaroori hai — wahi LLM(soch) aur Python(kaam) ke beech ka pul.
**D2.** Ek tool ki description jhoothi kar do to Claude **hamesha** galat tool chun
lega.
**Mera jawab:**
--- FALSE. "Hamesha" galat hai. Claude tool chunte waqt sirf ek desc nahi dekhta — tool ka
    NAAM + SAARE tools ki desc ek saath cross-check karta. Isliye ek jhoothi/colliding desc
    aksar use fool NAHI karti (aaj Try A me do baar sahi chuna). Reliable failure to under-scoped
    desc hai (Try B), jhoothi nahi.
### 🎯 Bonus (optional)

Tumhare **bajaj bot** me kuch users policy poochte hain ("foreclosure charge?"),
kuch live account poochte hain ("meri next EMI kab hai?"), aur kuch aisa jo bot ke
paas hai hi nahi ("aaj gold rate?"). Bina agent ke (Day 8 seedhi rassi) yeh teeno
ek jaisa handle hote the — problem kya thi? Agent lagane se har case me kya sudhrega?
Aur **kaise decide karoge** ki agent laga hi lena chahiye (hint: Day 12)?
**Mera jawab:**
--- Bina agent (Day 8 seedhi rassi) ki PROBLEM: teeno query ek hi raaste se jaati thi
    (retrieve -> Claude). Isliye:
      * "foreclosure charge?" -> theek (doc me hai).
      * "meri next EMI kab hai?" -> LIVE data, doc me hai hi nahi -> retrieve kachra /
        Claude hallucinate kar sakta (ek fake date bana de).
      * "aaj gold rate?" -> corpus se bahar -> kachra chunks + hallucination risk + token waste.
    Yaani 3 me se 2 queries galat raaste pe -> bad UX + jhoothe jawab ka khatra.
--- Agent lagane se har case:
      * policy sawaal  -> policy_search (RAG) tool.
      * next EMI       -> account_balance (live API) tool -> asli data.
      * gold rate      -> koi tool match nahi -> agent seedha "jaankari nahi hai" (self-correcting,
                          jhooth nahi) -> hallucination ruki.
    Yaani agent SAHI raasta chunta + out-of-scope pe imaandaar rehta.
--- Decide kaise (Day 12 eval, feeling se nahi):
      1. Baseline eval: Day 8 bot pe RAGAS/LLM-judge -> faithfulness, answer_relevancy
         (khaaskar next-EMI & gold-rate jaisi queries pe kitna hallucinate karta).
      2. Agent version pe wahi eval + "sahi tool chuna?" ka routing-accuracy check.
      3. Compare: agent me faithfulness/relevancy badhe (hallucination ghata) vs EXTRA cost
         (agent = har step ek LLM call = zyada latency + paisa).
      4. Rule: multi-source / live-data / out-of-scope wale bot me agent worth hai; ek hi
         source ke simple bot me overkill. Score theek badhe aur cost worth ho tabhi lagao.
    (Yehi Day 14 HyDE + Day 15 rerank ka sabak — koi bhi advanced cheez eval se prove karke lagao.)
