import task_manager
from task import Task
from prompt_toolkit import prompt, print_formatted_text, HTML, PromptSession
from prompt_toolkit.shortcuts import choice
from prompt_toolkit.completion import WordCompleter, Completer, Completion
import argparse
import pickle
import gcal_quickstart
from datetime import date, datetime, timedelta
from openai import OpenAI
import shlex


class CustomCompleter(Completer):
    flags = ["-category", "-due", "-children"]
    DATE_MAP: dict[str, date] = {
        "today": date.today(),
        "tomorrow": date.today() + timedelta(days=1),
        "next_week": date.today() + timedelta(days=7),
        "monday": date.today()
        + timedelta(days=((7 - date.today().weekday()) % 7) or 7),
        "tuesday": date.today()
        + timedelta(days=((8 - date.today().weekday()) % 7) or 7),
        "wednesday": date.today()
        + timedelta(days=((9 - date.today().weekday()) % 7) or 7),
        "thursday": date.today()
        + timedelta(days=((10 - date.today().weekday()) % 7) or 7),
        "friday": date.today()
        + timedelta(days=((11 - date.today().weekday()) % 7) or 7),
        "saturday": date.today()
        + timedelta(days=((12 - date.today().weekday()) % 7) or 7),
        "sunday": date.today()
        + timedelta(days=((13 - date.today().weekday()) % 7) or 7),
    }

    def __init__(self, categories, dates):
        self.categories = categories
        self.dates = dates

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        last_flag = None
        words = text.split()

        for i in range(len(words) - 1, -1, -1):  # reverse iterate to find last flag
            if words[i].startswith("-"):
                last_flag = words[i]
                break

        current_word = words[-1] if words else ""

        if current_word.startswith("-"):
            for flag in self.flags:
                if flag.startswith(current_word):
                    yield Completion(flag, start_position=-len(current_word))

        if last_flag == "-category":
            for category in self.categories:
                if category.startswith(current_word):
                    yield Completion(category, start_position=-len(current_word))

        if last_flag == "-due":
            for date_option in self.DATE_MAP.keys():
                if date_option.startswith(current_word):
                    yield Completion(date_option, start_position=-len(current_word))


def parse_task_input(input: str):
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "-name", required=True)
    parser.add_argument("-c", "-category")
    parser.add_argument("-d", "-due", required=True)
    parser.add_argument("-l", "-length")
    # recurrence interval in days currently
    # TODO: potentially explore ways to have a more flexible recurrence interval?
    parser.add_argument("-r", "-recurrence")
    # parses a list of arguments - separate child IDs with spaces
    parser.add_argument("-k", "-children", nargs="+")
    args = parser.parse_args(shlex.split(input))
    due_date_val = CustomCompleter.DATE_MAP.get(args.d)
    task = Task(
        name=args.n,
        due_date=datetime.combine(due_date_val, datetime.min.time())
        if due_date_val
        else None,
        category=args.c,
    )

    print("\n".join(task.get_receipt()))


# analyzes coming obligations from calendars and suggests preparatory tasks to complete in advance
def suggest_tasks_from_calendar(timespan: timedelta, auto_confirm: bool = True):
    calendar_tasks = gcal_quickstart.fetch_tasks_in_time_span(timespan)
    client = OpenAI(base_url="http://localhost:8080/v1", api_key="na")
    response = client.chat.completions.create(
        model="local",
        messages=[
            {
                "role": "user",
                "content": f"Analyze this list of calendar events: {calendar_tasks}. Identify upcoming obligations (e.g., exams, projects, deadlines, presentations). For each obligation, suggest preparatory tasks to complete a reasonable distance in advance, such as studying for exams, outlining projects, gathering resources, or practicing. Set reasonable due dates for these tasks before the obligation date. For each suggested task, provide a CLI command to create it, estimating duration in minutes. Format each command on a new line as: -n 'Task Name' -d 'YYYY-MM-DD' -c 'category' -l duration_minutes. Return only the commands, one per line.",
            }
        ],
        temperature=0.2,
        max_tokens=400,
    )
    tasks_data = response.choices[0].message.content
    if not tasks_data:
        print("No response from LLM.")
        return

    commands_list = []
    commands = tasks_data.strip().split("\n")
    for cmd in commands:
        cmd = cmd.strip()
        if not cmd:
            continue
        if not auto_confirm:
            print(f"Command: {cmd}")
            ans = input("Confirm? (y/n): ").strip().lower()
            if ans != "y":
                continue
        commands_list.append(cmd)
    print("Commands to run:")
    for cmd in commands_list:
        print(cmd)


# schudle tasks due for current day based on current gcal schedule
# if add breaks is True, add breaks between tasks where possible (default 15 minutes  )
def auto_schedule_tasks_for_day(add_breaks: bool = True, break_length: int = 15):
    # get current schedule from gcal
    gcal_schedule = gcal_quickstart.get_current_schedule_in_span(timedelta(days=1))
    # also load tasks from file
    tasks = task_manager.load_tasks_from_file()
    print(f"{gcal_schedule}")
    tasks_schedule = "\n".join(task.get_string_for_schedule() for task in tasks)
    print(tasks_schedule)
    client = OpenAI(base_url="http://100.104.230.28:8080/v1", api_key="na")
    response = client.chat.completions.create(
        model="local",
        messages=[
            {
                "role": "user",
                "content": f"Based on the current Google Calendar schedule: {gcal_schedule} and the pending tasks with their details: {tasks_schedule}, suggest optimal scheduling times for the tasks today. Avoid conflicts with existing calendar events, consider task durations and due dates, and add {break_length}-minute breaks between tasks if {add_breaks}. Return only a concise numbered list with task names and suggested start times. No explanations or additional text.",
            }
        ],
        temperature=0.2,
        max_tokens=400,
    )
    print("Suggested schedule from AI:")
    print(response.choices[0].message.content)


# create task objects in timespan with llm calendar analysis
# set confirm to True (default) to confirm before creating and saving task objects, false to add without confirmation
def llm_create_tasks(timespan: timedelta, confirm: bool = True):
    # need to get assignments from variety of sources:
    # Currently only from Google Calendar
    calendar_tasks = gcal_quickstart.fetch_tasks_in_time_span(timespan)
    client = OpenAI(base_url="http://localhost:8080/v1", api_key="na")
    response = client.chat.completions.create(
        model="local",
        messages=[
            {
                "role": "user",
                "content": f"Analyze this list of calendar events: {calendar_tasks}. Identify actionable tasks or assignments (e.g., homework, projects, deadlines, exams) that require completion, and ignore non-actionable events like lectures, classes, meetings, or informational sessions. For each actionable task, provide a CLI-style command to create it, estimating a reasonable completion time in minutes based on the task details. Format each command on a new line as: -n 'Task Name' -d 'YYYY-MM-DD' -c 'details' -l duration_minutes. If no due date, omit -d. Use today's date if due date not mentioned. Return only the commands, one per line.",
            }
        ],
        temperature=0.2,
        max_tokens=400,
    )
    tasks_data = response.choices[0].message.content
    if not tasks_data:
        print("No response from LLM.")
        return

    commands_list = []
    commands = tasks_data.strip().split("\n")
    for cmd in commands:
        cmd = cmd.strip()
        if not cmd:
            continue
        print(f"Command: {cmd}")
        ans = input("Confirm? (y/n): ").strip().lower()
        if ans == "y":
            commands_list.append(cmd)
    print("Confirmed commands to run:")
    for cmd in commands_list:
        print(cmd)


if __name__ == "__main__":
    print("Starting client...")
    auto_schedule_tasks_for_day()
    session = PromptSession()
    result = choice(
        message="Select an option:",
        options=[
            (1, "Add Task"),
            (2, "View Tasks"),
            (3, "Get task from Apriltag"),
            (4, "Suggest Prep Tasks from Obligations"),
        ],
    )
    if result == 1:
        task_manager.load_tasks_from_file()
        categories = task_manager.get_task_categories()

        with open("categories.pkl", "rb") as f:
            try:
                saved_categories = pickle.load(f)
                for cat in saved_categories:
                    if cat not in categories:
                        categories.append(cat)

            except Exception:
                pass

        print("Available categories:", categories)
        category_completer = WordCompleter(categories, ignore_case=True)
        completer = CustomCompleter(
            categories,
            [
                "tomorrow",
                "today",
            ],
        )
        task_input = session.prompt(
            "Enter task details: ",
            completer=completer,
        )
        with open("categories.pkl", "wb") as f:
            pickle.dump(categories, f)

        parse_task_input(task_input)

    elif result == 2:
        task_manager.load_tasks_from_file()
        if task_manager.task_tag_map is None or len(task_manager.task_tag_map) == 0:
            task_manager.assign_tags()
            task_manager.save_all_task_files()

        for task in task_manager.tasks:
            print("\n".join(task.get_receipt()))
    elif result == 3:
        tag_id_str = session.prompt("Enter Apriltag ID: ")
        try:
            tag_id = int(tag_id_str)
            task_manager.load_tasks_from_file()
            task = task_manager.task_tag_map.get(tag_id, None)
            if task is not None:
                print("\n".join(task.get_receipt()))
            else:
                print_formatted_text(
                    HTML(
                        f'<white bg="red">No task found for Apriltag ID: {tag_id}</white>'
                    )
                )
        except ValueError:
            print_formatted_text(
                HTML(
                    f'<white bg="red">Invalid Apriltag ID entered: {tag_id_str}</white>'
                )
            )
    elif result == 4:
        print("Analyzing obligations and suggesting preparatory tasks...")
        suggest_tasks_from_calendar(timedelta(days=4))
