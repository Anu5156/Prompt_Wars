from datetime import datetime, timedelta
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate():
    creds = None

    # Debug: show current files
    print("\n📂 Files in current directory:", os.listdir())

    # Load existing token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, login
    if not creds or not creds.valid:
        if not os.path.exists('my_credentials.json'):
            raise FileNotFoundError(
                "❌ 'my_credentials.json' not found in project folder."
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            'my_credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

        # Save token for reuse
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def create_events(schedule):
    try:
        creds = authenticate()
        service = build('calendar', 'v3', credentials=creds)

        start_time = datetime.now()

        print("\n📅 Creating events in Google Calendar...\n")

        for subject, minutes in schedule.items():
            minutes = int(minutes)

            end_time = start_time + timedelta(minutes=minutes)

            # 🔥 FINAL EVENT STRUCTURE WITH FIXED NOTIFICATION
            event = {
                'summary': f'Study: {subject}',
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Asia/Kolkata',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 0},  # ✅ exact start notification
                    ],
                },
            }

            service.events().insert(
                calendarId='primary',
                body=event
            ).execute()

            print(f"✅ Added: {subject} ({minutes} mins)")

            # Move to next time slot
            start_time = end_time

        print("\n🎉 All events successfully added to Google Calendar!")

    except Exception as e:
        print("\n❌ Error creating events:", e)