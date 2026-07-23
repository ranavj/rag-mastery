"""
Day 12 — File 1: RAG Evaluator KHUD banao (LLM-as-judge)
========================================================
Ab tak "jawab achha lag raha" = FEELING. Aaj NUMBER denge.

3 cheezein naapenge (har ek 0-1 score):
  1. Faithfulness      — jawab context pe based hai? (jhooth to nahi banaya = hallucination)
  2. Answer Relevance  — jawab sawaal ka hai? (idhar-udhar to nahi)
  3. Context Precision  — retrieved chunks relevant the? (kachra to nahi aaya)

Trick: "LLM as a judge" — ek LLM (Claude) se DOOSRE ke jawab ko judge karwao.
(Jaise exam checker — student ka answer dekh ke marks deta.)
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()


def judge(question, context, answer, metric_prompt):
    """Claude ko examiner banao — 0 se 1 score do."""
    prompt = (f"{metric_prompt}\n\n"
              f"QUESTION: {question}\n"
              f"CONTEXT: {context}\n"
              f"ANSWER: {answer}\n\n"
              f"Sirf ek number do 0.0 se 1.0 ke beech (aur kuch nahi).")
    resp = client.messages.create(model="claude-sonnet-4-6", max_tokens=10,
                                  messages=[{"role": "user", "content": prompt}])
    try:
        return float(resp.content[0].text.strip())
    except ValueError:
        return -1.0


def evaluate(question, context, answer):
    faith = judge(question, context, answer,
        "FAITHFULNESS naapo: kya ANSWER poori tarah CONTEXT pe based hai? "
        "Agar answer me koi baat hai jo context me NAHI, score kam do.")
    rel = judge(question, context, answer,
        "ANSWER RELEVANCE naapo: kya ANSWER seedha QUESTION ka jawab deta hai? "
        "Idhar-udhar ki baat ho to kam do.")
    return {"faithfulness": faith, "answer_relevance": rel}


if __name__ == "__main__":
    question = "What is the EMI bounce penalty?"
    context = "EMI Bounce Charge: Rs 1,000 + GST per bounced NACH/ECS mandate."

    # CASE 1 — achha jawab (context se, sahi)
    good = "EMI bounce hone par Rs 1,000 + GST charge lagta hai per mandate."
    # CASE 2 — bura jawab (hallucination — context me nahi tha!)
    bad = "EMI bounce par Rs 5,000 penalty aur account band ho jata hai."
    # CASE 3 — off-topic jawab (relevant nahi)
    off = "Bajaj Finance 1987 me shuru hui thi."

    print("=== RAG Evaluation (report card) ===\n")
    for label, ans in [("✅ ACHHA jawab", good),
                       ("❌ HALLUCINATED jawab", bad),
                       ("🤷 OFF-TOPIC jawab", off)]:
        scores = evaluate(question, context, ans)
        print(f"{label}: \"{ans[:50]}...\"")
        print(f"   faithfulness={scores['faithfulness']:.2f}  "
              f"answer_relevance={scores['answer_relevance']:.2f}\n")

    print("🎯 Ab 'achha lag raha' nahi — NUMBER hai. Hallucinated jawab ka faith score girega.")
