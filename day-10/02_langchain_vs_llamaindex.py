"""
Day 10 — File 2: LangChain vs LlamaIndex (same query, side-by-side)
===================================================================
Ek hi PDF, ek hi query — dono framework se. Taaki farak SAAF dikhe:
  - LangChain  = pieces khud jodo (flexible, "control do mujhe")
  - LlamaIndex = framework sab kare (kam code, "mujhpe chhod do")
Dono ka RESULT lagbhag same — bas ANDAAZ alag.
"""

import os
from dotenv import load_dotenv
load_dotenv()
BASE = os.path.dirname(__file__)
PDF = os.path.join(BASE, "bajaj_finance_policy_reference.pdf")
QUERY = "What is the penalty for EMI bounce?"

# ==================================================================
# APPROACH A — LangChain (Day 9 style): pieces khud jodo
# ==================================================================
def langchain_answer():
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    from langchain_anthropic import ChatAnthropic
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    docs = PyPDFLoader(PDF).load()                                    # load
    chunks = RecursiveCharacterTextSplitter(chunk_size=500,
             chunk_overlap=80).split_documents(docs)                 # chunk
    vs = Chroma.from_documents(chunks,
         SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"))# embed+store
    retriever = vs.as_retriever(search_kwargs={"k": 3})              # retriever
    prompt = ChatPromptTemplate.from_template(
        "Context:\n{context}\n\nQ: {question}\nA (short):")           # prompt
    llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=300)   # llm
    chain = ({"context": retriever | (lambda d: "\n".join(x.page_content for x in d)),
              "question": RunnablePassthrough()}
             | prompt | llm | StrOutputParser())                      # chain (jodo)
    return chain.invoke(QUERY)


# ==================================================================
# APPROACH B — LlamaIndex: framework sab sambhale
# ==================================================================
def llamaindex_answer():
    from llama_index.core import VectorStoreIndex, Settings
    from llama_index.readers.file import PDFReader
    from llama_index.llms.langchain import LangChainLLM
    from langchain_anthropic import ChatAnthropic
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    Settings.llm = LangChainLLM(llm=ChatAnthropic(model="claude-sonnet-4-6", max_tokens=300))
    Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")

    docs = PDFReader().load_data(file=PDF)                # load
    index = VectorStoreIndex.from_documents(docs)         # chunk+embed+store (ek line!)
    engine = index.as_query_engine(similarity_top_k=3)    # retriever+prompt+llm (packed)
    return str(engine.query(QUERY))                       # query


if __name__ == "__main__":
    print(f"❓ QUERY: {QUERY}\n")
    print("=" * 60)
    print("A) LangChain — ~10 lines (pieces khud jode):")
    print("=" * 60)
    print(langchain_answer()[:300], "...\n")

    print("=" * 60)
    print("B) LlamaIndex — ~4 lines (framework sab kiya):")
    print("=" * 60)
    print(llamaindex_answer()[:300], "...\n")

    print("🎯 Same RAG, same jawab — LangChain = control, LlamaIndex = convenience.")
