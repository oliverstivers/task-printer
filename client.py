from task_manager import TaskManager
from task import Task
from prompt_toolkit import prompt, print_formatted_text, HTML, PromptSession
from prompt_toolkit.shortcuts import choice
from prompt_toolkit.completion import WordCompleter, Completer, Completion
import argparse
import pickle
from datetime import date, timedelta
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
    parser.add_argument("-k", "-children", nargs='+')
    args = parser.parse_args(shlex.split(input))
    task = Task(
        name=args.n, due_date=CustomCompleter.DATE_MAP.get(args.d), category=args.c
    )

    print("\n".join(task.get_receipt()))


# fetches tasks from connected calendars from the current time until time specified by timespan
def recommend_tasks_from_calendars(timespan: timedelta):
    pass


# create task objects in timespan with llm calendar analysis
# set confirm to True (default) to confirm before creating and saving task objects, false to add without confirmation
def llm_create_tasks(timespan: timedelta, confirm: bool = True):
    pass


if __name__ == "__main__":
    print("Starting client...")
    session = PromptSession()
    result = choice(
        message="Select an option:",
        options=[(1, "Add Task"), (2, "View Tasks"), (3, "Get task from Apriltag")],
    )
    if result == 1:
        TaskManager.load_tasks_from_file()
        categories = TaskManager.get_task_categories()

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
        TaskManager.load_tasks_from_file()
        if TaskManager.task_tag_map is None or len(TaskManager.task_tag_map) == 0:
            TaskManager.assign_tags()
            TaskManager.save_all_task_files(TaskManager.tasks)

        for task in TaskManager.tasks:
            print("\n".join(task.get_receipt()))
    elif result == 3:
        tag_id_str = session.prompt("Enter Apriltag ID: ")
        try:
            tag_id = int(tag_id_str)
            TaskManager.load_tasks_from_file()
            task = TaskManager.task_tag_map.get(tag_id, None)
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
