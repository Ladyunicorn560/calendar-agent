# ✅ frontend/app.py

import sys
import os
import streamlit as st

# Add backend to path so we can import from it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from langgraph_agent import build_graph

graph = build_graph()

st.set_page_config(page_title="🧠 Calendar Agent")
st.title("📅 Conversational Booking Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input field
if prompt := st.chat_input("Ask to check or book a meeting..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        state = {"messages": st.session_state.messages}
        result = graph.invoke(state)
        response = str(result.get("tool", "⚠️ Couldn't understand the request."))
    except Exception as e:
        response = f"❌ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
