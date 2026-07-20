"""
Day 6 — File 1: PDF se text nikaalna (low-level, pypdf se khud)
================================================================
PDF binary format hai — f.read() se kachra milta (khud dekha humne!).
pypdf woh "parser" hai jo PDF ke compressed streams decode karke text deta.

Yahan hum PAGE-BY-PAGE khud extraction karenge — taaki dikhe:
  - PDF = pages ki list (har page alag object)
  - har page se .extract_text() -> plain text
  - page number TRACK karna humari zimmedari (yahi metadata banega!)

Frontend analogy: pypdf = ek parser lib (jaise CSV-parse ya cheerio HTML ke liye).
Format ka expert — use karo, khud binary mat samjho.
"""

import os
from pypdf import PdfReader

PDF_PATH = os.path.join(os.path.dirname(__file__), "sample_docs",
                        "bajaj_finance_policy_reference.pdf")   # path lesson (Day 5!)

# ---- STEP 1: PDF kholo ----
reader = PdfReader(PDF_PATH)
print(f"📄 PDF khuli: {os.path.basename(PDF_PATH)}")
print(f"   Total pages: {len(reader.pages)}")
print(f"   Metadata: {reader.metadata}")   # PDF ki apni info (author, creator...)

# ---- STEP 2: har page se text nikalo (page-by-page loop) ----
all_pages = []
for page_num, page in enumerate(reader.pages, start=1):
    text = page.extract_text()             # <- yahi hai asli "decode" moment
    all_pages.append({"page": page_num, "text": text})
    print(f"\n--- Page {page_num} ({len(text)} chars) — pehle 150 chars: ---")
    print(text[:150].strip())

# ---- STEP 3: dekho kya mila — ab yeh NORMAL text hai ----
total_chars = sum(len(p["text"]) for p in all_pages)
print(f"\n✅ Total extracted: {total_chars} chars from {len(all_pages)} pages")
print("   Ab yeh plain text hai — Day 3 chunking + Day 5 Chroma ismein plug ho sakte!")
