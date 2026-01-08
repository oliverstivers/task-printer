from datetime import datetime, timedelta, timezone
import os.path

from google.auth.transport.requests import Request
import pytz
from openai import OpenAI
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


# authorize and return events from google calendar with calendar id and in timespan
def get_events_from_calendar(calendarId: str, timespan: timedelta = timedelta(days=1)):
    list_of_tasks: list[str] = []
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.now(pytz.timezone("America/Los_Angeles")).isoformat()
        events_result = (
            service.events()
            .list(
                calendarId=calendarId,
                timeMin=now,
                timeMax=(datetime.now(tz=timezone.utc) + timespan).isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return []

        calendar_details = service.calendars().get(calendarId=calendarId).execute()
        calendar_name = calendar_details.get("summary")
        print(
                f"Getting the upcoming events in specified time span: {timespan.days} days from calendar: {calendar_name} "
        )
        # Prints the start and name of the next 10 events
        for event in events:
            start = datetime.fromisoformat(event["start"].get("dateTime", event["start"].get("date"))).astimezone(pytz.timezone("America/Los_Angeles"))
            end = datetime.fromisoformat(event["end"].get("dateTime", event["end"].get("date"))).astimezone(pytz.timezone("America/Los_Angeles"))
            list_of_tasks.append(f"{start} - {event['summary']}")
            print(start, end, event["summary"])
        return list_of_tasks
    except HttpError as error:
        print(f"An error occurred: {error}")
    return list_of_tasks


def get_current_schedule_in_span(timespan: timedelta) -> list[str]:
    """Return scheduled tasks from personal google calendar. Includes things like appointments, class schedule, and anything else I want to schedule tasks around"""
    schedule: list[str] = get_events_from_calendar("oliverstivers@gmail.com", timespan)
    print(schedule)
    return schedule
    pass


def fetch_tasks_in_time_span(timespan: timedelta) -> list[str]:
    """Fetch tasks from Google Calendar within the specified time span"""
    list_of_tasks = get_events_from_calendar(
        "5avmj6pmsm2h3mekqof53ddaan7ksaiv@import.calendar.google.com", timespan
    )
    

if __name__ == "__main__":
    fetch_tasks_in_time_span(timedelta(days=4))
    print("----------------")
    get_current_schedule_in_span(timedelta(days=4))
