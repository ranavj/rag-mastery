"""
Agent tools (THE differentiator, Day 17-18).  (Day 22)

  - policy_search : Day 21 RAG ko wrap karta (docs se jawab + citations)
  - account_api   : mock LIVE data (balance / EMI / status)

Design: tools ko `company_id` + citations wapas chahiye, par agent tool ko sirf ek
STRING deta. Isliye FACTORY — har request pe company_id closure me bind + `state` dict
me sources capture (React useCallback dependency close-over jaisa).

Descriptions = LAKSHMAN REKHA (Day 17-18 seekh: na tight na dheeli — warna agent galat
tool chune ya bhookha reh ke hallucinate kare).
"""

from langchain_core.tools import tool

from app.generation.rag_chain import answer as rag_answer

# mock "live" account DB (Day 22). Asli API baad me plug hoga.
_FAKE_ACCOUNTS = {
    "VJ-100": "Account VJ-100 → outstanding balance ₹12,500 | next EMI ₹3,200 due 5 Aug 2026 | status ACTIVE",
    "VJ-200": "Account VJ-200 → outstanding balance ₹0 | loan CLOSED | koi dues nahi",
}


def build_tools(company_id: str, state: dict):
    """company_id (closure) + state (sources capture) ke saath tools banao."""

    @tool
    def policy_search(query: str) -> str:
        """Company ke policy/documents me general sawaal ka jawab dhoondho — charges, rules,
        process, EMI/foreclosure/prepayment policy waghairah. Kisi SPECIFIC user ke live
        account data (balance/EMI-due/status) ke liye ye tool NAHI."""
        text, sources = rag_answer(query, company_id)
        state["sources"] = sources
        return text

    @tool
    def account_api(account_id: str) -> str:
        """Ek SPECIFIC user ke LIVE account ka data do — outstanding balance, next EMI due,
        ya loan status. Input = account id jaise 'VJ-100'. Sirf tab jab user apne account/
        balance/EMI-due/status ki baat kare (general policy ke liye ye NAHI)."""
        return _FAKE_ACCOUNTS.get(
            account_id, f"Account '{account_id}' hamare system me nahi mila."
        )

    return [policy_search, account_api]
