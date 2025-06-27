# 🗓️ Conversational Calendar Agent

An AI-powered assistant that helps users book appointments through natural language via Google Calendar.

### 🔗 Live Demo
👉 [Try it here](https://calendar-agent-kdqdgjy2yetgfv9fvduqgw.streamlit.app/)

### ⚙️ Tech Stack
- Python + FastAPI
- LangGraph (for agent framework)
- Streamlit (frontend chat)
- Google Calendar API

### 💡 Features
- Natural language understanding
- Checks Google Calendar availability
- Suggests and books slots
- Conversational UI with chat flow

### 📁 Structure
- `frontend/app.py`: Streamlit interface  
- `backend/calendar_utils.py`: Google Calendar logic  
- `backend/langgraph_agent.py`: LangGraph agent setup  

### 🔐 Note
Secrets (like API keys) are stored securely in Streamlit Cloud and not exposed in this repo.

---
