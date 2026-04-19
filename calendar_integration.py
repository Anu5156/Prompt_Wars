"""
📘 FILE: calendar_integration.py

📅 PURPOSE:
Integrates study schedule with Google Calendar.

🔗 FUNCTION:
create_events(time_slots)

📥 INPUT:
Generated timetable

📤 OUTPUT:
Creates calendar events

⚙️ REQUIREMENTS:
- Google API credentials
- OAuth setup

💡 BENEFIT:
- Real-world usability
- Automated reminders

🚀 FUTURE:
Can support:
- Notifications
- Sync across devices
"""

from datetime import datetime, timedelta
import os.path
import logging

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 🔧 Logging setup
logging.basicConfig(level=logging.INFO)

# 🔐 Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# 🎨 Priority → Color mapping (Google Calendar color IDs)
PRIORITY_COLORS = {
    "high": "11",    # red
    "medium": "5",   # yellow
    "low": "2"       # green
}


def get_calendar_service():
    """
    Authenticates user and returns Google Calendar service.
    """

    creds = None

    # 🔁 Load existing token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # 🔐 If not valid → authenticate
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'my_credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def create_events(time_slots):
    """
    Creates Google Calendar events for given time slots.

    Args:
        time_slots (list): List of slots with subject, start, end, day

    Returns:
        int: Number of events successfully created
    """

    logging.info("Creating calendar events...")

    service = get_calendar_service()

    base_date = datetime.now().date()
    event_count = 0

    for slot in time_slots:
        try:
            # 🧠 Safe day handling
            day_value = slot.get("day", "Day 1")

            if isinstance(day_value, str) and "Day" in day_value:
                day_num = int(day_value.split()[-1])
            else:
                day_num = 1

            event_date = base_date + timedelta(days=day_num - 1)

            # ⏰ Time parsing
            start_time = datetime.strptime(slot["start"], "%H:%M").time()
            end_time = datetime.strptime(slot["end"], "%H:%M").time()

            start_datetime = datetime.combine(event_date, start_time).isoformat()
            end_datetime = datetime.combine(event_date, end_time).isoformat()

            subject = slot["subject"]

            # 🎯 Detect priority from subject (default = medium)
            # (You can improve this later if you pass priorities)
            priority = "medium"
            color_id = PRIORITY_COLORS.get(priority, "5")

            # 📅 Event object
            event = {
            'summary': slot['subject'],
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            # 🔥 ADD THIS BLOCK
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 60},
                    {"method": "popup", "minutes": 30},
                    {"method": "popup", "minutes": 10},
                    {"method": "popup", "minutes": 1}
    ]
}
        }
            # 🚀 Insert event
            service.events().insert(calendarId='primary', body=event).execute()
            event_count += 1

        except Exception as e:
            logging.error(f"❌ Error creating event: {e}")

    logging.info(f"✅ {event_count} events added to calendar")
    return event_count