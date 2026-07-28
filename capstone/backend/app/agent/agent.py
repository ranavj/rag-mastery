"""
Agent executor — LLM khud tool chunta (Day 17-18).  (Day 22)

REUSE: create_tool_calling_agent + AgentExecutor + prompt {agent_scratchpad}.
`tool_used` intermediate_steps se nikaalte (agent ne asli kya chuna) → ChatResponse.
"""

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from app.agent.tools import build_tools
from app.config import ANTHROPIC_API_KEY, CLAUDE_MODEL

_llm = ChatAnthropic(model=CLAUDE_MODEL, api_key=ANTHROPIC_API_KEY, temperature=0)

_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Tum SmartSupport ka support agent ho. Jawab dene ke liye diye gaye tools use karo.\n"
            "- Policy/charges/rules/process ke sawaal → policy_search.\n"
            "- Kisi account ka balance/EMI-due/status → account_api.\n"
            "Agar kisi tool se sahi jawab na mile, ya sawaal in dono me na aaye, to honestly "
            "bolo ki jaankari nahi hai. Kuch bhi apne se mat banao (no hallucination).",
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


def run_agent(question: str, company_id: str) -> tuple[str, list[dict], str]:
    """returns (answer, sources, tool_used). Har request pe fresh tools (company_id bound)."""
    state: dict = {"sources": []}
    tools = build_tools(company_id, state)

    agent = create_tool_calling_agent(_llm, tools, _prompt)
    executor = AgentExecutor(agent=agent, tools=tools, return_intermediate_steps=True)
    result = executor.invoke({"input": question})

    # agent ne asli kaunse tool chalaye? (intermediate_steps = har step ka action)
    tools_used = [action.tool for action, _obs in result.get("intermediate_steps", [])]
    if "account_api" in tools_used:
        tool_used = "account_api"
    elif "policy_search" in tools_used:
        tool_used = "policy_search"
    else:
        tool_used = "none"

    # citations sirf policy_search ke case me meaningful
    sources = state["sources"] if tool_used == "policy_search" else []
    return _as_text(result["output"]), sources, tool_used


def _as_text(output) -> str:
    """Claude ka output kabhi list-of-content-blocks hota hai — string me normalize."""
    if isinstance(output, str):
        return output
    if isinstance(output, list):
        return "".join(
            b.get("text", "") if isinstance(b, dict) else str(b) for b in output
        )
    return str(output)
