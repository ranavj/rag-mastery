"""
Day 17-18 — Agentic RAG (FROM SCRATCH)
======================================
Ab tak: query -> retrieve -> Claude -> jawab  (ek SEEDHI RASSI, har baar same).
Aaj    : query -> LLM KHUD sochta hai kaunsa TOOL chalana hai -> chalao ->
         result wapas LLM ko -> LLM aur chahiye to dobara tool, warna final jawab.
         (Ek LOOP, self-correcting. RAG ab bas EK tool hai agent ke haath me.)

Asli "jaadu" (Vijay ne khud pakda 😎):
   LLM sirf RAW STRING deta hai ("policy_search chalao"). Woh khud function
   nahi chala sakta. Hum us string ko PROGRAM me PARSE karte hain aur sahi
   Python function call karte hain. Bas yahi agent loop hai.

Do tools is demo me:
   1) policy_search(q)   -> HAMARA RAG (bajaj policy chunks retrieve). Real doc.
   2) account_balance(x) -> ek FAKE account "API/DB" (live data, doc me ho hi
                            nahi sakta). Dikhata hai: har query retrieve ka kaam
                            nahi — kuch queries ko doosra raasta chahiye.

Description = LLM ke liye tool ka "manual" (role + kaam + LIMIT). LLM isi ko
padh ke tool chunta hai (Day 11 router ki description wali soch, agla level).
"""

import os
import re
import numpy as np
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
emb_model = SentenceTransformer("all-MiniLM-L6-v2")
client = Anthropic()
MODEL = "claude-sonnet-4-6"


# ===========================================================================
# PART A — Do choti "duniya": (1) policy corpus for RAG, (2) fake account DB
# ===========================================================================

# (1) Bajaj-style policy docs — yeh HAMARA RAG tool retrieve karega.
POLICY_DOCS = [
    "EMI bounce policy. Agar EMI bounce ho ya auto-debit fail ho to Rs 1000 ke "
    "saath GST ka bounce charge lagta hai, jo agli EMI ke saath vasool hota hai. "
    "Baar-baar bounce se CIBIL score girta hai.",
    "Foreclosure policy. Loan time se pehle band karna foreclosure hai. Personal "
    "loan par foreclosure charge outstanding principal ka 4 percent plus GST hai.",
    "Late payment policy. Due date ke baad 3 din grace period. Uske baad har din "
    "late fee, jo outstanding ka 2 percent prati maah tak ja sakta hai.",
]
POLICY_VECS = emb_model.encode(POLICY_DOCS, normalize_embeddings=True)

# (2) Ek FAKE account database (dict). Yeh LIVE data hai — kisi policy PDF me
#     ho hi nahi sakta. Isliye ise retrieve NAHI kar sakte; API/DB chahiye.
ACCOUNTS_DB = {
    "VJ-100": {"name": "Vijay", "balance": 42500, "next_emi": "2026-08-05"},
    "VJ-200": {"name": "Riya",  "balance":  1800, "next_emi": "2026-08-12"},
}


# ===========================================================================
# PART B — TOOLS. Har tool = ek Python function. Description = LLM ka manual.
# ===========================================================================

def policy_search(query: str) -> str:
    """Hamara RAG: query embed -> cosine -> top-2 policy chunks laut do."""
    qv = emb_model.encode([query], normalize_embeddings=True)[0]
    scores = POLICY_VECS @ qv                      # cosine (normalized dot)
    top = np.argsort(scores)[::-1][:2]             # top-2
    return "\n".join(f"- {POLICY_DOCS[i]}" for i in top)


def account_balance(account_id: str) -> str:
    """Fake API: account_id daalo, live balance/next EMI wapas. Doc me nahi milta."""
    acc = ACCOUNTS_DB.get(account_id.strip())
    if not acc:
        return f"Account '{account_id}' nahi mila."
    return (f"{acc['name']} | balance Rs {acc['balance']} | "
            f"next EMI {acc['next_emi']}")


# Tool registry: naam -> (function, description). LLM ko YEH describe karenge.
TOOLS = {
    "policy_search": (
        policy_search,
        "Bajaj loan POLICY ke sawaal: EMI bounce charge, foreclosure charge, "
        "late payment fee, grace period. Input = sawaal (text). "
        "Account balance ya live account data ke liye NAHI.",
    ),
    "account_balance": (
        account_balance,
        "Kisi account ka LIVE balance aur next EMI date. "
        "Input = account id (jaise 'VJ-100'). "
        "Policy/charges ke sawaal ke liye NAHI.",
    ),
}


# ===========================================================================
# PART C — AGENT LOOP. Yeh dil hai. LLM decide, hum parse+chalao, wapas do.
# ===========================================================================

def build_system_prompt() -> str:
    """LLM ko tools batao + protocol batao (kis format me jawab de)."""
    tool_lines = "\n".join(
        f"- {name}: {desc}" for name, (_, desc) in TOOLS.items()
    )
    return f"""Tum ek assistant ho jiske paas yeh TOOLS hain:
{tool_lines}

Har turn me EK line me EXACTLY isi format me jawab do:
   TOOL: <tool_name> | INPUT: <tool ka input>
   -- ya agar tumhare paas ab final jawab hai --
   ANSWER: <final jawab user ke liye>

Rule: agar sawaal tools se bahar hai (jaise mausam), tool mat chalao,
seedha "ANSWER: mujhe iski jaankari nahi hai" bolo. Ek baar me ek hi step."""


# Yeh regex hi "raw string -> function call" ka pul hai (Vijay wali baat).
TOOL_RE = re.compile(r"TOOL:\s*(\w+)\s*\|\s*INPUT:\s*(.+)", re.IGNORECASE | re.DOTALL)
ANS_RE  = re.compile(r"ANSWER:\s*(.+)", re.IGNORECASE | re.DOTALL)


def run_agent(user_query: str, max_steps: int = 4, verbose: bool = True) -> str:
    """Manual ReAct loop: sochna(LLM) -> karna(tool) -> phir sochna -> ... -> jawab."""
    system = build_system_prompt()
    # 'messages' = agent ki chalti-firti memory (kya-kya hua ab tak).
    messages = [{"role": "user", "content": user_query}]

    for step in range(1, max_steps + 1):
        # 1) LLM SOCHTA hai (tools + ab tak ka itihaas dekh ke).
        reply = client.messages.create(
            model=MODEL, max_tokens=400, system=system, messages=messages,
        ).content[0].text.strip()
        if verbose:
            print(f"\n  [step {step}] LLM bola: {reply}")

        # 2) Kya LLM ne final ANSWER diya? -> loop khatam.
        m_ans = ANS_RE.search(reply)
        if m_ans and not TOOL_RE.search(reply):
            return m_ans.group(1).strip()

        # 3) Warna LLM ne TOOL maanga. String PARSE karo -> asli function chalao.
        m_tool = TOOL_RE.search(reply)
        if not m_tool:
            return reply  # format toota, jo mila wahi de do
        tool_name, tool_input = m_tool.group(1).strip(), m_tool.group(2).strip()

        fn = TOOLS.get(tool_name, (None,))[0]
        if fn is None:
            observation = f"'{tool_name}' naam ka koi tool nahi hai."
        else:
            observation = fn(tool_input)          # <<< yahan RAG/API chalta hai
        if verbose:
            print(f"  [step {step}] tool '{tool_name}' chala -> {observation}")

        # 4) Tool ka result wapas LLM ko do (memory me daalo) -> agla turn.
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user",
                         "content": f"TOOL RESULT ({tool_name}): {observation}\n"
                                    f"Ab isse user ko jawab do ya agla tool chalao."})

    return "Max steps ho gaye, pakka jawab nahi bana."


# ===========================================================================
# PART D — DEMO. Teen alag query, teen alag raasta (agent khud chunega).
# ===========================================================================
if __name__ == "__main__":
    queries = [
        "EMI bounce hone par kitna charge lagta hai?",   # -> policy_search (RAG)
        "Mere account VJ-100 me kitna balance hai?",      # -> account_balance (API)
        "Aaj Delhi ka mausam kaisa hai?",                 # -> koi tool nahi
    ]
    for q in queries:
        print("\n" + "=" * 70)
        print("USER:", q)
        ans = run_agent(q)
        print("\n>>> FINAL:", ans)
