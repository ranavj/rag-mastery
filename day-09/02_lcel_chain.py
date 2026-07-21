"""
Day 9 — File 2: Asli LangChain LCEL chain (RAGBot ka framework version)
=======================================================================
Day 8 ka manual ask() (vanilla) -> ab ek declarative CHAIN (framework).
Wahi RAG, saaf andaaz:  retriever | prompt | llm | parser

Har piece LangChain ka "Runnable" hai (usme wahi __or__ magic hai jo humne
File 1 mein khud banaya). '|' unhe ek assembly-line mein jodta hai.
"""

import os
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()
BASE = os.path.dirname(__file__)

# ---- pieces (har ek ek "station") ----

# 1. RETRIEVER — Day 6 ka bajaj_policy collection (LangChain wrapper)
emb = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(collection_name="bajaj_policy", embedding_function=emb,
                     persist_directory=os.path.join(BASE, "..", "day-06", "chroma_db"))
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 2. PROMPT — template (jaise ek React component with {props})
prompt = ChatPromptTemplate.from_template(
    """Tum Bajaj Finance helpdesk ho. SIRF CONTEXT se jawab do (Hinglish, short).
Na ho to bolo "jaankari nahi hai".

CONTEXT:
{context}

SAWAAL: {question}""")

# 3. LLM — Claude (LangChain wrapper)
llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=400)

# 4. PARSER — LLM ke response object se sirf text nikalo
parser = StrOutputParser()

# retrieved docs ko ek string mein jodne wala chhota helper
def format_docs(docs):
    return "\n\n".join(f"[page {d.metadata.get('page','?')}] {d.page_content}" for d in docs)


# ---- THE CHAIN (poora RAG ek line mein) ----
# {context, question} banao -> prompt bharo -> llm -> text nikalo
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | parser
)
# RunnablePassthrough = user ka question jaisa hai waise aage bhej do (unchanged)


if __name__ == "__main__":
    print("=== LCEL chain (framework version) ===")
    print("chain = {context: retriever|format, question: passthrough} | prompt | llm | parser\n")

    for q in ["What is the penalty for EMI bounce?", "What is the price of a pizza?"]:
        print(f"👤 {q}")
        print(f"🤖 {chain.invoke(q)}\n")

    print("🎯 Day-8 ka 40-line ask() ab ek CHAIN mein — wahi kaam, framework andaaz.")
