"""
Day 16 — Multi-Query + Parent-Child Chunking (FROM SCRATCH)
===========================================================
Do alag problem, do alag fix — dono ek pipeline me:

1) MULTI-QUERY  : 1 query -> LLM se 3-4 ROOP -> sab search -> merge (unique).
                  Kyun? User ek cheez kai wording me poochta hai; ek "unlucky"
                  wording sahi doc miss kar sakti hai. Kai roop = recall UP.
                  (Cost BADHTA hai: 1 extra LLM call + kai search. Optional tool.)

2) PARENT-CHILD : Trade-off ka jugaad ->
                  - chhota chunk = search me SATIK (focused embedding)
                  - bada chunk   = LLM ko POORA context
                  Fix: search CHILD (chhota) pe, par LLM ko do PARENT (bada).
                  "Dhoondha child se, diya parent." (Day 15/14 wala pattern:
                   jis pe search karo zaroori nahi wahi LLM ko do.)

Ingestion (data daalte waqt): doc ko DO baar todo ->
   split #1: bade PARENTS   -> ek simple dict (docstore) me (NO embedding)
   split #2: har parent ke chhote CHILDREN -> embed karke search-store me
Har child apne parent ka `parent_id` yaad rakhta hai (foreign key / pointer).
"""

import os
import re
import numpy as np
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
emb_model = SentenceTransformer("all-MiniLM-L6-v2")
client = Anthropic()


# ---------------------------------------------------------------------------
# 0) Corpus — Bajaj-style policy paragraphs. Har ek ek PARENT (bada) hai.
#    Dhyaan do: har parent me KAI baatein hain (isliye bada = search dhundhla,
#    par context pura).
# ---------------------------------------------------------------------------
PARENT_DOCS = [
    # P-0
    "EMI bounce / payment fail policy. Agar aapki EMI bounce ho jaati hai ya "
    "auto-debit fail hota hai to Rs 1000 ke saath GST ka bounce charge lagta hai. "
    "Yeh charge agli EMI ke saath vasool kiya jaata hai. Baar baar bounce hone par "
    "aapka CIBIL score bhi girta hai.",
    # P-1
    "Late payment aur penalty policy. Due date ke baad 3 din ka grace period milta "
    "hai. Uske baad har din ka late fee lagta hai jo outstanding amount ka 2 percent "
    "prati maah tak ja sakta hai. Grace period ke andar payment par koi penalty nahi.",
    # P-2
    "Prepayment aur foreclosure policy. Loan ko time se pehle band karna foreclosure "
    "kehlata hai. Personal loan par foreclosure charge outstanding principal ka 4 "
    "percent plus GST hai. Part-prepayment saal me do baar bina charge allowed hai.",
    # P-3
    "Delivery aur shipping policy. Standard delivery 5 se 7 working din leti hai. "
    "Express delivery 2 din me poori hoti hai. Delivery ka status app se track hota hai.",
]
# Parent ids: P-0, P-1, ...
PARENT_IDS = [f"P-{i}" for i in range(len(PARENT_DOCS))]


# ---------------------------------------------------------------------------
# 1) INGESTION — do-level split
#    docstore  = { parent_id : parent_text }   (NO embedding, bas lookup ke liye)
#    children  = [ {id, text, parent_id} ]     (INKO embed karenge)
# ---------------------------------------------------------------------------
def split_into_children(text):
    """Parent ko chhote children me todo. Scratch me: sentence-wise (simple).
    (Real me RecursiveCharacterTextSplitter — Day 3 wala.)"""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if len(p.strip()) > 0]


docstore = {}          # parent_id -> parent text  (yeh hai "dict" jisme parent rehta)
children = []          # har child: dict(id, text, parent_id)

for pid, ptext in zip(PARENT_IDS, PARENT_DOCS):
    docstore[pid] = ptext                       # parent ko docstore me daalo
    for j, ctext in enumerate(split_into_children(ptext)):
        children.append({"id": f"{pid}-c{j}", "text": ctext, "parent_id": pid})

# SIRF children ko embed karo (Chroma ki jagah scratch me numpy array)
child_vecs = emb_model.encode([c["text"] for c in children])

print(f"Ingest done: {len(docstore)} parents (docstore) | "
      f"{len(children)} children (embedded)\n")


# ---------------------------------------------------------------------------
# 2) MULTI-QUERY — LLM se ek query ke kai roop banwao
# ---------------------------------------------------------------------------
def multi_query(query, n=3):
    prompt = (
        f"Neeche ek user question hai. Isi matlab ke {n} alag-alag tareeke se "
        f"likhe hue versions do (alag shabd, same meaning). Sirf {n} lines, "
        f"har line ek question, koi number ya bullet nahi.\n\nQuestion: {query}"
    )
    resp = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    lines = [l.strip("-• ").strip() for l in resp.content[0].text.splitlines()]
    variants = [l for l in lines if l]
    return [query] + variants          # original + roop (original bhi rakho)


# ---------------------------------------------------------------------------
# 3) RETRIEVE — har roop ki search CHILD pe -> merge unique -> parent lookup
# ---------------------------------------------------------------------------
def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def search_children(q, top_k=2):
    qv = emb_model.encode(q)
    scored = [(cosine(qv, child_vecs[i]), i) for i in range(len(children))]
    scored.sort(reverse=True)
    return [i for _, i in scored[:top_k]]      # top_k child indexes


def retrieve(query):
    queries = multi_query(query)
    print("MULTI-QUERY roop:")
    for q in queries:
        print(f"   • {q}")

    # sab roop ki search -> child indexes ka set (MERGE + unique)
    hit_child_idx = set()
    for q in queries:
        for i in search_children(q):
            hit_child_idx.add(i)
    print(f"\nMatched CHILDREN (unique): "
          f"{[children[i]['id'] for i in hit_child_idx]}")

    # child -> uske parent_id -> docstore se PARENT uthao (lookup, search nahi)
    parent_ids = []
    for i in hit_child_idx:
        pid = children[i]["parent_id"]
        if pid not in parent_ids:              # parent bhi unique
            parent_ids.append(pid)
    print(f"Unique PARENTS to return: {parent_ids}\n")

    return [docstore[pid] for pid in parent_ids]


# ---------------------------------------------------------------------------
# 4) GENERATE — poore PARENTS ko context bana ke Claude se jawab
# ---------------------------------------------------------------------------
def answer(query):
    parents = retrieve(query)
    context = "\n\n".join(parents)
    prompt = (
        "Neeche di gayi POLICY ke aadhar par hi jawab do (Hinglish, short). "
        "Agar jawab policy me nahi hai to 'jaankari nahi mili' bolo.\n\n"
        f"POLICY:\n{context}\n\nSawaal: {query}"
    )
    resp = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()


if __name__ == "__main__":
    q = "EMI bounce hone pe kitna charge lagega?"
    print(f"USER QUERY: {q}\n" + "-" * 60)
    ans = answer(q)
    print("-" * 60)
    print("ANSWER:", ans)
