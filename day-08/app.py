"""
Day 8 — Streamlit UI (browser chat) — engine ko import karke
=============================================================
Streamlit = Python se web-UI banane ka tool. Har widget ek line.
Note: Streamlit script har interaction pe POORA dobara chalta (top-to-bottom) —
isliye "state" (chat history, bot) ko st.session_state mein rakhte hain
(bilkul React ke useState jaisa — warna har render pe reset ho jaye).

Run:  streamlit run day-08/app.py
"""

import os
import streamlit as st
from rag_bot import RAGBot

st.set_page_config(page_title="Bajaj Policy Bot", page_icon="🤖")
st.title("🤖 Bajaj Finance Policy Bot")
st.caption("RAG over an actual 12-page policy PDF · answers cite the page")

# --- bot ko ek baar banao + ingest (session_state = React useState jaisa) ---
if "bot" not in st.session_state:
    with st.spinner("Policy ingest ho rahi hai (ek baar)..."):
        bot = RAGBot()
        bot.ingest(os.path.join(os.path.dirname(__file__),
                                "sample_docs", "bajaj_finance_policy_reference.pdf"))
        st.session_state.bot = bot
        st.session_state.messages = []   # chat history

# --- purani chat dobara dikhao (script har baar re-run hota) ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- input box (neeche fixed) ---
if query := st.chat_input("Policy ke baare mein poochein... (e.g. EMI bounce penalty?)"):
    # user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # bot answer
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hun..."):
            out = st.session_state.bot.ask(query)
        answer = out["answer"]
        if out["sources"]:
            answer += f"\n\n---\n📄 *Source: policy.pdf — page(s) {out['sources']}*"
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
