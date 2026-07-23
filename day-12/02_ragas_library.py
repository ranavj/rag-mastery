"""
Day 12 — File 2: Asli RAGAS (professional RAG evaluation)
=========================================================
Humara scratch judge 2 metrics deta tha. RAGAS ready metrics deti hai
+ teesra (context precision = retrieval quality).

3 metrics:
  - faithfulness      : jawab context pe based? (hallucination)
  - answer_relevancy  : jawab sawaal ka?
  - context_precision : retrieved context relevant tha? (RETRIEVAL naapo)

RAGAS default OpenAI use karta — humein Claude + local embeddings plug karna padta
(jaise Day 10 me LlamaIndex me kiya — frameworks interconnect).
"""

import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_anthropic import ChatAnthropic
from langchain_community.embeddings import SentenceTransformerEmbeddings
from dotenv import load_dotenv

load_dotenv()

# RAGAS ko Claude + local embeddings do (OpenAI ki jagah)
llm = LangchainLLMWrapper(ChatAnthropic(model="claude-sonnet-4-6", max_tokens=500))
emb = LangchainEmbeddingsWrapper(SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"))

# ---- Eval dataset: har row = ek "test case" (jaise unit test) ----
# question + jo chunks retrieve hue + jo answer bana + (ground truth optional)
data = {
    "question": [
        "What is the EMI bounce penalty?",
        "What is the EMI bounce penalty?",
    ],
    "contexts": [   # retrieved chunks (list of lists)
        ["EMI Bounce Charge: Rs 1,000 + GST per bounced NACH/ECS mandate."],
        ["EMI Bounce Charge: Rs 1,000 + GST per bounced NACH/ECS mandate."],
    ],
    "answer": [
        "EMI bounce par Rs 1,000 + GST charge lagta hai per mandate.",   # ACHHA
        "EMI bounce par Rs 5,000 penalty aur account band ho jata hai.", # HALLUCINATED
    ],
    # reference = "sahi jawab" (ground truth) — context_precision ise chahiye
    # (jaise unit test me expected value)
    "reference": [
        "EMI bounce par Rs 1,000 + GST charge lagta hai.",
        "EMI bounce par Rs 1,000 + GST charge lagta hai.",
    ],
}
dataset = Dataset.from_dict(data)

# ---- Evaluate (RAGAS metrics chalao) ----
print("📊 RAGAS chal raha hai (har metric ke liye LLM judge)...\n")
result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
    llm=llm,
    embeddings=emb,
)

print("=== RAGAS Report Card ===")
df = result.to_pandas()
for i, row in df.iterrows():
    label = "✅ ACHHA" if i == 0 else "❌ HALLUCINATED"
    print(f"\n{label}: \"{row['response'][:50]}...\"")   # RAGAS: answer -> response
    print(f"   faithfulness      = {row['faithfulness']:.2f}")
    print(f"   answer_relevancy  = {row['answer_relevancy']:.2f}")
    print(f"   context_precision = {row['context_precision']:.2f}")

print("\n🎯 Scratch se same idea — bas RAGAS ready + teesra metric (context_precision).")
