"""
Day 11 — File 1: Query Router KHUD banao (embedding-based)
==========================================================
Kahani: reception pe baithi ladki — har sawaal sun ke sahi department bhejti.
Router = wahi "receptionist" — query dekh ke decide kare kaunsa SOURCE.

Frontend analogy: React Router — URL dekh ke sahi component. Yahan URL ki jagah
query ka MEANING, aur route embedding se decide hota (semantic routing).

Flow: query → ROUTER (kaunsa source?) → us source pe retrieve → chunks
"""

import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


# ---- 3 alag knowledge sources (har ek chhota) ----
SOURCES = {
    "HR": {
        "description": "Employee leave policy, salary, working hours, holidays, attendance",
        "docs": [
            "Casual leave: 12 din per year. Sick leave: 8 din.",
            "Working hours: 9:30 AM to 6:30 PM, Monday to Friday.",
            "Salary credit har month ki last working day ko hota hai.",
        ],
    },
    "FINANCE": {
        "description": "Loan EMI, interest rate, refund, payment, bounce charges",
        "docs": [
            "EMI bounce charge: Rs 1,000 + GST per bounced mandate.",
            "Personal loan interest rate 12% se shuru hoti hai.",
            "Refund 30 din ke andar process hota hai.",
        ],
    },
    "TECH": {
        "description": "IT support, password reset, VPN, laptop, software, email setup",
        "docs": [
            "Password reset: portal.company.com/reset par jao.",
            "VPN connect karne ke liye GlobalProtect app use karo.",
            "Naya laptop request IT ticket se hoti hai.",
        ],
    },
}

# ---- har source ke DESCRIPTION ko embed kar lo (yahi router ka "menu") ----
source_names = list(SOURCES.keys())
source_vecs = model.encode([SOURCES[s]["description"] for s in source_names])


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ---- ROUTER: query ko sabse-milte-julte source pe bhejo ----
def route(query: str) -> str:
    q_vec = model.encode(query)
    scores = [cosine(q_vec, sv) for sv in source_vecs]      # har source se similarity
    best = int(np.argmax(scores))                           # sabse zyada = wahi source
    return source_names[best], scores


# ---- us source ke andar retrieve (simple cosine) ----
def retrieve_from(source: str, query: str, top_k=1):
    docs = SOURCES[source]["docs"]
    q_vec = model.encode(query)
    doc_vecs = model.encode(docs)
    scores = [cosine(q_vec, dv) for dv in doc_vecs]
    ranked = sorted(range(len(docs)), key=lambda i: scores[i], reverse=True)
    return [docs[i] for i in ranked[:top_k]]


# ---- DEMO ----
if __name__ == "__main__":
    queries = [
        "Mujhe kitni chhutti milti hai?",       # HR
        "EMI bounce hone par kitna charge?",    # FINANCE
        "Password kaise reset karun?",          # TECH
    ]

    for q in queries:
        source, scores = route(q)
        print(f"👤 {q}")
        print(f"   🚦 Router → {source}  (scores: " +
              ", ".join(f"{n}={s:.2f}" for n, s in zip(source_names, scores)) + ")")
        chunk = retrieve_from(source, q)[0]
        print(f"   📄 {chunk}\n")

    print("🎯 Router ne bina jawab diye — sirf sahi SOURCE choose kiya (receptionist!).")
