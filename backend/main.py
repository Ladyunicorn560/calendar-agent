from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime, timedelta
from .calendar_utils import authenticate_google, check_availability, book_meeting



app = FastAPI()
service = authenticate_google()

class AvailabilityRequest(BaseModel):
    start_time: str  # ISO format
    end_time: str    # ISO format

class BookingRequest(BaseModel):
    summary: str
    start_time: str
    end_time: str

@app.post("/check_availability")
def check_slot(req: AvailabilityRequest):
    start_dt = datetime.fromisoformat(req.start_time)
    end_dt = datetime.fromisoformat(req.end_time)
    events = check_availability(service, start_dt, end_dt)
    return {"available": len(events) == 0, "events": events}

@app.post("/book_meeting")
def book(req: BookingRequest):
    start_dt = datetime.fromisoformat(req.start_time)
    end_dt = datetime.fromisoformat(req.end_time)
    link = book_meeting(service, req.summary, start_dt, end_dt)
    return {"status": "success", "link": link}
