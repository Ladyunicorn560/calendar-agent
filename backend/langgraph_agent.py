import os
import datetime
import dateparser
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import Tool, initialize_agent, AgentType
from langgraph.graph import StateGraph, END
from typing import TypedDict
from calendar_utils import check_availability, book_meeting, authenticate_google
from dateparser.search import search_dates

load_dotenv()

class AgentState(TypedDict):
    messages: list
    tool: str

# Tool: parse natural language time using dateparser
def extract_datetimes(text: str, default_duration_minutes: int = 30):
    parsed_dates = search_dates(text)
    if not parsed_dates:
        raise ValueError("Could not parse any date from input.")
    if len(parsed_dates) == 1:
        start = parsed_dates[0][1]
        end = start + datetime.timedelta(minutes=default_duration_minutes)
    else:
        start = parsed_dates[0][1]
        end = parsed_dates[1][1]
    return start, end


def build_graph():
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model_name="llama3-8b-8192", groq_api_key=api_key)
    service = authenticate_google()

    def availability_tool(input_text: str) -> str:
        try:
            start_dt, end_dt = extract_datetimes(input_text)
            events = check_availability(service, start_dt, end_dt)
            return f"✅ Available: {len(events) == 0} from {start_dt} to {end_dt}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def booking_tool(input_text: str) -> str:
        try:
            start_dt, end_dt = extract_datetimes(input_text)
            link = book_meeting(service, "Meeting", start_dt, end_dt)
            return f"📅 Meeting booked: {link}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    tools = [
        Tool(name="check_availability", func=availability_tool, description="Check availability from natural language."),
        Tool(name="book_meeting", func=booking_tool, description="Book a meeting from natural language.")
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    def call_agent(state: AgentState):
        input_text = state["messages"][-1]["content"]
        result = agent.run(input_text)
        return {"messages": state["messages"], "tool": result}

    builder = StateGraph(AgentState)
    builder.add_node("agent", call_agent)
    builder.set_entry_point("agent")
    builder.add_edge("agent", END)

    return builder.compile()
