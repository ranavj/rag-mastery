"""
Day 11 — File 2: LLM-based Router (Claude decide karta)
========================================================
File 1 mein router EMBEDDING se decide karta tha (weak model = galti).
Ab LLM (Claude) se — woh "chhutti = leave = HR" ka MEANING achhe se samajhta.

Yeh AGENTS ki jhalak hai: LLM sirf jawab nahi de raha — DECIDE kar raha
(kaunsa source). Course ke agents se seedha connection.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

# Same 3 sources (File 1 wale)
SOURCES = {
    "HR":      "Employee leave, chhutti, salary, working hours, holidays, attendance",
    "FINANCE": "Loan EMI, interest rate, refund, paisa wapas, bounce charges, payment",
    "TECH":    "IT support, password reset, VPN, laptop, software, email setup",
}


# ---- LLM ROUTER: Claude ko sources do, woh sahi chune ----
def route_llm(query: str) -> str:
    menu = "\n".join(f"- {name}: {desc}" for name, desc in SOURCES.items())
    prompt = (f"Ek user query ko sahi department pe route karo.\n\n"
              f"DEPARTMENTS:\n{menu}\n\n"
              f"QUERY: {query}\n\n"
              f"Sirf ek department ka NAAM likho (HR/FINANCE/TECH), aur kuch nahi.")
    resp = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=10,
        messages=[{"role": "user", "content": prompt}])
    return resp.content[0].text.strip().upper()


if __name__ == "__main__":
    queries = [
        "Mujhe kitni chhutti milti hai?",        # HR (File 1 me weak model atka tha)
        "EMI bounce hone par kitna charge?",     # FINANCE
        "Password kaise reset karun?",           # TECH
        "Mera paisa wapas kab aayega?",          # FINANCE (koi 'refund' shabd nahi!)
    ]

    for q in queries:
        source = route_llm(q)
        print(f"👤 {q}")
        print(f"   🚦 LLM Router → {source}\n")

    print("🎯 Claude ne MEANING samajh ke route kiya (weak embedding se nahi atka).")
    print("   Aur — LLM yahan DECIDE kar raha, sirf jawab nahi de raha = agents ki jhalak!")
