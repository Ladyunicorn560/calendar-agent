# backend/calendar_utils.py

from __future__ import print_function
import datetime
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None

    # Use Streamlit secrets to read credentials (secure and cloud-friendly)
    creds_data = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

    # Token path — works locally; safe fallback if not present
    token_path = "credentials/token.json"
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh or authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(creds_data, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token (optional: only locally useful)
        os.makedirs("credentials", exist_ok=True)
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

def check_availability(service, start_time, end_time):
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_time.isoformat() + "Z",
        timeMax=end_time.isoformat() + "Z",
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    return events_result.get("items", [])

def book_meeting(service, summary, start_time, end_time):
    event = {
        "summary": summary,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    return event.get("htmlLink")
