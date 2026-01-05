from datetime import datetime, timedelta, timezone
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def fetch_tasks_in_time_span(timespan: timedelta) -> list[str]:
    """ Fetch tasks from Google Calendar within the specified time span
    """
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
        now = datetime.now(tz=timezone.utc).isoformat()
        print("Getting the upcoming events in specified time span: ", timespan)
        events_result = (
            service.events()
            .list(
                calendarId="5avmj6pmsm2h3mekqof53ddaan7ksaiv@import.calendar.google.com",
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

        # Prints the start and name of the next 10 events
        list_of_tasks = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            list_of_tasks.append(f"{start} - {event['summary']}")
            print(start, event["summary"])
        return list_of_tasks
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    fetch_tasks_in_time_span(timedelta(days=4))
