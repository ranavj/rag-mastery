"""
Generation: retrieved chunks + Claude -> grounded answer + citations.  (Day 21)

REUSE: Day 8 (grounding + honest "not found"), Day 9 (LCEL: prompt|llm|parser).
Double guard: (1) retriever threshold khaali de → NOT_FOUND; (2) prompt Claude ko
context ke bahar jaane se rokta (agar chunk aaye par jawab na ho tab bhi honest).
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from app.retrieval.retriever import retrieve

NOT_FOUND = "Is baare me mujhe aapke documents me jaankari nahi mili."

_llm = ChatAnthropic(model=CLAUDE_MODEL, api_key=ANTHROPIC_API_KEY, temperature=0)

_prompt = ChatPromptTemplate.from_template(
    """Tum ek support assistant ho. SIRF neeche diye CONTEXT se jawab do.
Agar jawab context me nahi hai, to saaf bolo: "{not_found}"
Apne aap se koi jaankari mat jodo (no hallucination). Jawab short + user ki bhaasha me.

CONTEXT:
{context}

SAWAAL: {question}

JAWAB:"""
)

_chain = _prompt | _llm | StrOutputParser()   # Day 9 LCEL


def answer(question: str, company_id: str) -> tuple[str, list[dict]]:
    """returns (answer_text, sources). sources = citations (Day 6 metadata)."""
    hits = retrieve(question, company_id)

    if not hits:                              # guard 1: threshold ne sab reject kiya
        return NOT_FOUND, []

    context = "\n\n".join(f"[page {h['page']}] {h['text']}" for h in hits)
    ans = _chain.invoke(
        {"context": context, "question": question, "not_found": NOT_FOUND}
    )

    sources = [
        {"text": h["text"][:200], "page": h["page"], "doc_id": h["doc_id"]}
        for h in hits
    ]
    return ans, sources
