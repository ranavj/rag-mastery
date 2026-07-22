"""
Day 10 — LlamaIndex se RAG (doosra framework)
==============================================
Kahani: LangChain = general store (aap pieces jodo). LlamaIndex = RAG-specialist
store 🦙 (documents do, poocho — baaki woh sambhale).

LlamaIndex ka mental model — bahut chhota:
    Documents  →  Index (auto: chunk+embed+store)  →  Query Engine  →  query()

Compare: Day 9 LangChain = retriever|prompt|llm|parser (4 pieces khud jode).
         LlamaIndex     = index.as_query_engine().query(q)  (framework sab kare).
"""

import os
from llama_index.core import VectorStoreIndex, Settings
from llama_index.readers.file import PDFReader
from llama_index.llms.langchain import LangChainLLM      # LangChain LLM ko LlamaIndex me plug
from langchain_anthropic import ChatAnthropic            # Day 9 wala, already working
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv

load_dotenv()
BASE = os.path.dirname(__file__)

# ---- Settings: ek jagah batao kaunsa LLM + embedding (global config) ----
# NOTE: humara Claude LangChain ChatAnthropic se, LlamaIndex me wrap karke (version-clash bacha)
Settings.llm = LangChainLLM(llm=ChatAnthropic(model="claude-sonnet-4-6", max_tokens=400))
Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")  # wahi Day-2 model
# NOTE: LlamaIndex me embedding+chunking ki default settings andar hi hoti hain

# ---- STEP 1: Documents load (LlamaIndex ka apna PDF reader) ----
docs = PDFReader().load_data(file=os.path.join(BASE, "bajaj_finance_policy_reference.pdf"))
print(f"📄 Loaded: {len(docs)} document objects")

# ---- STEP 2: Index banao — YAHI MAGIC hai ----
# ek line me: chunk + embed + store — sab andar ho jata (Day 3+2+5 sab packed!)
index = VectorStoreIndex.from_documents(docs)
print("🔧 Index ready (chunk+embed+store — sab is ek line me hua)")

# ---- STEP 3: Query Engine — retriever + prompt + llm sab EK me packed ----
query_engine = index.as_query_engine(similarity_top_k=3)
print("🤖 Query engine ready\n")

# ---- STEP 4: Poocho (Day 9 ka poora chain = ab ek .query() call) ----
for q in ["What is the penalty for EMI bounce?",
          "What is the minimum CIBIL score for a personal loan?"]:
    print(f"👤 {q}")
    response = query_engine.query(q)
    print(f"🤖 {response}\n")
    # response ke andar source nodes bhi hote (citations) — dekhte hain:
    pages = {n.metadata.get("page_label", "?") for n in response.source_nodes}
    print(f"   📄 source pages: {sorted(pages)}\n")

print("🎯 Compare: LangChain me 4 pieces khud jode. LlamaIndex ne sab sambhal liya (kam code).")
