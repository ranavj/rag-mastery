"""
Day 16 — File 2: Multi-Query + Parent-Child with LangChain (library version)
============================================================================
Scratch (File 1) me humne HAATH se kiya tha:
  - do-level split (parents -> children), ek `dict` docstore
  - children embed, `parent_id` pointer
  - multi_query() : LLM se roop banwana
  - retrieve()    : har roop ki child-search -> merge unique -> parent lookup

LangChain in sabko DO wrappers me chhupa deta hai:

  1. ParentDocumentRetriever  = poora Parent-Child mechanism
       - child_splitter se children banata + vectorstore(Chroma) me embed
       - parents ko docstore (InMemoryStore = wahi `dict`) me rakhta
       - .invoke(q): child pe search -> unke PARENTS return  (lookup andar chhupa)

  2. MultiQueryRetriever      = poora Multi-Query mechanism
       - LLM se query ke roop banata + har roop base-retriever pe chalata
       - results MERGE + unique karta  (humara set() logic andar chhupa)

JOD kaise? MultiQueryRetriever ke ANDAR base retriever = ParentDocumentRetriever.
Yaani: roop banao -> har roop child-search -> parents lao -> sab merge. Bilkul
File 1 wala flow, bas loop/dict/merge dikh nahi rahe (wrapper=abstraction).
"""

import re
import logging
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.retrievers import ParentDocumentRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

# MultiQueryRetriever apne banaye ROOP ko INFO log pe print karta hai -> ON karo
# taaki File 1 ki tarah "multi-query roop" aankhon se dikhein.
logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)


# ---- Same corpus jaisa File 1 (har string ek PARENT = bada policy paragraph) ----
PARENT_DOCS = [
    "EMI bounce / payment fail policy. Agar aapki EMI bounce ho jaati hai ya "
    "auto-debit fail hota hai to Rs 1000 ke saath GST ka bounce charge lagta hai. "
    "Yeh charge agli EMI ke saath vasool kiya jaata hai. Baar baar bounce hone par "
    "aapka CIBIL score bhi girta hai.",
    "Late payment aur penalty policy. Due date ke baad 3 din ka grace period milta "
    "hai. Uske baad har din ka late fee lagta hai jo outstanding amount ka 2 percent "
    "prati maah tak ja sakta hai. Grace period ke andar payment par koi penalty nahi.",
    "Prepayment aur foreclosure policy. Loan ko time se pehle band karna foreclosure "
    "kehlata hai. Personal loan par foreclosure charge outstanding principal ka 4 "
    "percent plus GST hai. Part-prepayment saal me do baar bina charge allowed hai.",
    "Delivery aur shipping policy. Standard delivery 5 se 7 working din leti hai. "
    "Express delivery 2 din me poori hoti hai. Delivery ka status app se track hota hai.",
]
docs = [Document(page_content=t) for t in PARENT_DOCS]


# ---------------------------------------------------------------------------
# 1) PARENT-CHILD setup  (ParentDocumentRetriever)
# ---------------------------------------------------------------------------
emb = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# vectorstore = CHILDREN yahan embed honge (File 1 ka child_vecs)
vectorstore = Chroma(collection_name="day16_pc", embedding_function=emb)

# docstore = PARENTS yahan (File 1 ka `docstore` dict; InMemoryStore = wahi dict)
docstore = InMemoryStore()

# child_splitter = split #2 (parent -> chhote children). parent_splitter=None =>
# har input Document KHUD ek parent (File 1 jaisa: 4 policy = 4 parent).
child_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)

parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,      # children (search yahan)
    docstore=docstore,            # parents (lookup yahan)
    child_splitter=child_splitter,
    search_kwargs={"k": 2},       # har query par top-2 child -> unke parents
)
# add_documents ANDAR: parent ko docstore me daala + children bana ke embed kiya
# + har child me parent ka id daala (pointer). Poori File-1 ingestion, 1 line me.
parent_retriever.add_documents(docs)


# ---------------------------------------------------------------------------
# 2) MULTI-QUERY setup  (MultiQueryRetriever ke andar parent_retriever)
# ---------------------------------------------------------------------------
llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=300)

mq_parent_retriever = MultiQueryRetriever.from_llm(
    retriever=parent_retriever,   # <-- base = Parent-Child retriever
    llm=llm,                      # <-- yeh LLM query ke roop banayega
)


# ---------------------------------------------------------------------------
# 2b) 🐛 BUG + FIX  — default parser ka keeda aur uska ilaaj
# ---------------------------------------------------------------------------
# BUG: MultiQueryRetriever ka DEFAULT parser har newline ko ek query maan leta
#      hai. LLM aksar upar ek intro line deta hai jaise:
#          "Here are 3 different versions of the question:"
#      Wo bekaar line bhi "query" ban ke search ho jaati -> galat/extra doc aata
#      -> PRECISION girti hai. (File 1 scratch me humne khud strip kiya tha, isliye
#       ye keeda nahi aaya — scratch-first ka fayda.)
#
# FIX: apna output parser do jo (a) numbering/bullets hataye, (b) intro line
#      (jo ':' pe khatam hoti ya '?' pe nahi) ko chhaan de. Sirf asli sawaal rakhe.
class CleanLineParser(BaseOutputParser):
    """Har line ko saaf karo; preamble/intro line phenk do."""
    def parse(self, text):
        out = []
        for line in text.strip().splitlines():
            line = re.sub(r"^\s*\d+[\.\)]\s*", "", line)   # "1." / "2)" hatao
            line = line.strip("-• ").strip()
            if not line:
                continue
            if line.endswith(":"):                          # "...versions:" intro
                continue
            if "?" not in line:                             # sawaal hi nahi to chhodo
                continue
            out.append(line)
        return out


CLEAN_PROMPT = PromptTemplate(
    input_variables=["question"],
    template=(
        "User ke question ke 3 alag-alag versions do (alag shabd, same matlab). "
        "SIRF 3 sawaal do, har ek apni line par. Koi intro, number ya bullet mat "
        "likho — pehli line se hi sawaal shuru ho.\n\nQuestion: {question}"
    ),
)

# LCEL chain: prompt | llm | apna parser  -> seedha saaf list of queries deta hai
clean_chain = CLEAN_PROMPT | llm | CleanLineParser()

mq_parent_retriever_fixed = MultiQueryRetriever(
    retriever=parent_retriever,
    llm_chain=clean_chain,        # <-- default ki jagah apna saaf chain
)


# ---------------------------------------------------------------------------
# 3) Chalao — DEFAULT (buggy) vs FIXED, side by side
# ---------------------------------------------------------------------------
def show(name, retriever, query):
    parents = retriever.invoke(query)
    print(f"\n[{name}] -> {len(parents)} PARENT docs:")
    for i, d in enumerate(parents, 1):
        preview = d.page_content[:60].replace("\n", " ")
        print(f"   {i}. {preview}...")


if __name__ == "__main__":
    query = "EMI bounce hone pe kitna charge lagega?"
    print(f"USER QUERY: {query}")

    # (dono ke generated-queries INFO log me upar print honge)
    show("DEFAULT parser (buggy)", mq_parent_retriever, query)
    show("CLEAN parser (fixed)", mq_parent_retriever_fixed, query)
