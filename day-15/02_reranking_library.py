"""
Day 15 — File 2: Re-ranking with LangChain (library version)
============================================================
Scratch (File 1) me humne 3 kaam HAATH se kiye:
  1. bi-encoder cosine -> shortlist
  2. cross-encoder loop (har pair pe predict)
  3. re-sort -> top final_k

LangChain in teenon ko 2 wrapper me chhupata hai:
  - CrossEncoderReranker            = Stage 2 (loop + sort ANDAR)
  - ContextualCompressionRetriever  = base retriever (Stage 1) + reranker jodta
                                      -> ek hi .invoke(query)

"Compression" naam kyun? Kyunki base se aaye bade candidate set ko reranker
NICHOD ke (compress) sirf best top_n rakhta. (filter + re-sort = compression.)

Same SonicWave corpus (File 1 wala) -> dekhte hain library bhi wahi flip deta hai.
"""

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# Same corpus jaisa File 1 (D0 = sahi jawab, lambe doc me daba; D1 = echo-trap)
DOCS = [
    ("Founded in 2012, our audio company designs premium speakers loved by customers worldwide. From compact "
     "travel units to large home theatre systems, we focus on rich sound and long-lasting build quality. "
     "The SonicWave model keeps going for about eighteen hours before it needs to be plugged in again."),      # D0 SAHI
    "The number of hours a speaker can play on one charge usually depends on the volume level you choose.",     # D1 echo-trap
    "Details about how many hours each speaker plays on a single charge are printed on the retail box.",        # D2 echo-trap
    "The SonicWave speaker is available in three colours and supports the latest Bluetooth 5.0 standard.",      # D3 model naam, jawab nahi
    "Standard shipping usually takes 5 to 7 working days for most delivery locations across the country.",      # D4 off-topic
]
QUERY = "How many hours does the SonicWave speaker play on one charge?"

# ---- Stage 1 setup: bi-encoder embeddings + Chroma vectorstore (in-memory) ----
emb = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_texts(DOCS, embedding=emb, collection_name="day15_rerank")

# base_retriever = Stage 1 (bi-encoder cosine). k=4 => shortlist (extra candidates).
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ---- Stage 2 setup: cross-encoder reranker ----
ce_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-12-v2")
reranker = CrossEncoderReranker(model=ce_model, top_n=2)     # top_n = final_k

# ContextualCompressionRetriever = Stage1 (base) + Stage2 (reranker) ek saath
compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever,
)


def show(title, docs):
    print(f"\n{title}")
    for rank, d in enumerate(docs, 1):
        print(f"  {rank}. {d.page_content[:65]}...")


if __name__ == "__main__":
    print(f"QUERY: {QUERY}")

    # BEFORE re-ranking = sirf base retriever (Stage 1, rough)
    show("STAGE 1 only — base retriever (bi-encoder, rough):",
         base_retriever.invoke(QUERY))

    # AFTER re-ranking = compression retriever (Stage 1 + Stage 2)
    show("STAGE 1 + 2 — compression retriever (re-ranked, sateek):",
         compression_retriever.invoke(QUERY))

    print("\n(Scratch File 1 jaisa hi flip — par yahan loop/sort LangChain ke andar chhupe hain.)")
