"""
Day 17-18 — Agentic RAG (LIBRARY / LangChain)
=============================================
File 1 (scratch) me humne KHUD banaya tha:
   - system prompt jisme tools describe kiye
   - "TOOL: x | INPUT: y" format + regex se PARSE
   - loop: LLM -> tool chalao -> result wapas -> phir LLM
   - messages[] = agent ki memory

LangChain me yeh POORA loop `AgentExecutor` ke andar chhup jaata hai (bilkul
Day 15 ke ContextualCompressionRetriever / Day 16 ke ParentDocumentRetriever
jaisa — "loop andar chhupa"). Hum sirf 3 cheez dete hain:
   1) tools  (@tool decorator — function ka docstring hi DESCRIPTION ban jaata hai)
   2) llm    (ChatAnthropic, jo "tool calling" karna jaanta hai)
   3) prompt (thoda sa instruction + jagah jahan agent apni soch rakhega)

DHYAAN: yahan hum "TOOL: ... | INPUT: ..." wala format KHUD nahi likhte.
Claude ka native "tool use" feature LangChain use karta hai — LLM structured
tool-call bhejta hai, LangChain parse karke function chalata hai. Wahi scratch
wala parsing, ab framework ke andar.

BONUS (aaj ka 🐛): DESCRIPTION_BUG = True -> policy_search ki description ko
UNDER-SCOPED (bahut sankuchit) kar do: "sirf foreclosure, EMI bounce ke liye
NAHI". Ab "EMI bounce charge?" query pe agent ke paas koi valid tool nahi
bachta -> woh "jaankari nahi" bol deta hai, JABKI jawab data me maujood tha.
=> description = tool ki LAKSHMAN REKHA. Zyada narrow = tool bhookha reh jaata,
   RAG chalta hi nahi (Day 11 router ki galat description jaisa asli bug).

LIVE OBSERVATION (imaandaari): pehle humne ULTA try kiya tha — description ko
JHOOTHA/colliding banaya (balance tool ne bola "main policy ka hoon"). Do baar
try kiya, Claude ne DONO baar SAHI tool chuna! Kyun? tool ka NAAM + SAARE tools
ki descriptions ek saath cross-check hote hain -> ek jhoothi line fool nahi
karti. Modern tool-calling robust hai. Reliable failure = UNDER-SCOPING (upar).
"""

import numpy as np
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
emb_model = SentenceTransformer("all-MiniLM-L6-v2")

# --- ek description ko jaan-boojh ke bigaad ke bug dekhne ke liye ---------
DESCRIPTION_BUG = False   # <<< True: policy_search under-scoped -> tool bhookha (RAG chalta hi nahi)


# ===========================================================================
# Duniya: policy corpus (RAG) + fake account DB  (File 1 jaisa hi)
# ===========================================================================
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

ACCOUNTS_DB = {
    "VJ-100": {"name": "Vijay", "balance": 42500, "next_emi": "2026-08-05"},
    "VJ-200": {"name": "Riya",  "balance":  1800, "next_emi": "2026-08-12"},
}


# ===========================================================================
# TOOLS — @tool. Function ka DOCSTRING hi LLM ke liye description ban jaata hai.
# (File 1 me humne TOOLS dict me alag se description likhi thi; yahan docstring.)
# ===========================================================================
def _run_policy_search(query: str) -> str:
    """Asli RAG kaam (description se alag rakha, taaki bug me sirf desc badle)."""
    qv = emb_model.encode([query], normalize_embeddings=True)[0]
    scores = POLICY_VECS @ qv
    top = np.argsort(scores)[::-1][:2]
    return "\n".join(f"- {POLICY_DOCS[i]}" for i in top)


if not DESCRIPTION_BUG:
    @tool
    def policy_search(query: str) -> str:
        """Bajaj loan POLICY ke sawaal: EMI bounce charge, foreclosure charge,
        late payment fee, grace period. Input = sawaal (text). Live account
        balance ke liye NAHI."""
        return _run_policy_search(query)
else:
    # 🐛 UNDER-SCOPED description: kaam wahi (poora policy corpus search) par
    #    description ne daayra sikod diya -> "sirf foreclosure, EMI bounce NAHI".
    #    Ab EMI bounce query is tool ko chhuegi hi nahi -> RAG bhookha.
    @tool
    def policy_search(query: str) -> str:
        """SIRF foreclosure / prepayment charge ke sawaal ke liye. Input =
        sawaal (text). EMI bounce, late payment ya balance ke liye NAHI."""
        return _run_policy_search(query)


@tool
def account_balance(account_id: str) -> str:
    """Kisi account ka LIVE balance aur next EMI date. Input = account id
    (jaise 'VJ-100'). Policy/charges ke sawaal ke liye NAHI."""
    acc = ACCOUNTS_DB.get(account_id.strip())
    if not acc:
        return f"Account '{account_id}' nahi mila."
    return (f"{acc['name']} | balance Rs {acc['balance']} | "
            f"next EMI {acc['next_emi']}")


TOOLS = [policy_search, account_balance]


# ===========================================================================
# AGENT banao — 3 cheez: prompt + llm + tools. Loop AgentExecutor ke andar.
# ===========================================================================
llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=500)

# {agent_scratchpad} = woh jagah jahan agent apni soch + tool results rakhta hai
# (File 1 ke messages[] ka framework version). Yeh placeholder ZAROORI hai.
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tum ek Bajaj assistant ho. Diye gaye tools soch-samajh ke "
               "istemal karo. Agar sawaal tools se bahar hai (jaise mausam), "
               "tool mat chalao — seedha bolo jaankari nahi hai."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, TOOLS, prompt)
# verbose=True -> andar ka LOOP dikhega (kaunsa tool, kya input, kya result).
executor = AgentExecutor(agent=agent, tools=TOOLS, verbose=True)


# ===========================================================================
# DEMO
# ===========================================================================
if __name__ == "__main__":
    print("DESCRIPTION_BUG =", DESCRIPTION_BUG, "\n")
    queries = [
        "EMI bounce hone par kitna charge lagta hai?",   # -> policy_search
        "Mere account VJ-100 me kitna balance hai?",      # -> account_balance
    ]
    for q in queries:
        print("\n" + "=" * 70)
        print("USER:", q)
        result = executor.invoke({"input": q})
        print(">>> FINAL:", result["output"])
