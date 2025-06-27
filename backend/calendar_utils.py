# backend/calendar_utils.py

from __future__ import print_function
import datetime
import os
import json
from googleapiclient.discovery import build
import streamlit as st
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/calendar']

from google.oauth2 import service_account

def authenticate_google():
    creds_data = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

    credentials = service_account.Credentials.from_service_account_info(
        creds_data,
        scopes=SCOPES
    )

    return build("calendar", "v3", credentials=credentials)


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
