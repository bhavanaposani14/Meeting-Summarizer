"""
Google Calendar sync (optional).  Called after save_meeting().
Requires a service‑account json or OAuth creds file dropped at /config/gcal.json
and ENABLE_GCAL=true in .env.
"""
from google.oauth2 import service_account
from googleapiclient.discovery import build
from .settings import get_settings
from datetime import datetime
import pytz

settings = get_settings()
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def _service():
    creds = service_account.Credentials.from_service_account_file(
        "/config/gcal.json", scopes=SCOPES
    )
    return build("calendar", "v3", credentials=creds)

async def attach_summary(event_id: str, summary: str, calendar_id="primary"):
    if not settings.ENABLE_GCAL:
        return
    svc = _service()
    event = svc.events().get(calendarId=calendar_id, eventId=event_id).execute()
    notes = event.get("description", "")
    event["description"] = f"{notes}\n\n===== AI SUMMARY =====\n{summary}"
    svc.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
