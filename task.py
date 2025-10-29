# Copyright (c) 2025 Oliver Stivers
# Licensed under the MIT License. See LICENSE file in the project root for full license text.


import datetime, timedelta
import tabulate
import uuid


# Each task will represent something i have to do
# can have subtasks, everything will either have a due date or a time that it will be done
# potentailly have some sort of distinction between tasks that are "reminders" (i.e. midterm on this day, essay)
# "reminders" can have subtasks and methods to generate
# we should keep track of a print time that controls when the task is printed, can be set explicitly or automatically
class Task:
    _due_date = None
    _duration = 0
    _task_id = None
    _print_time = None
    _task_name = None
    _task_category = ""
    _parent_id = None
    _child_id = None

    def __init__(self, name, due_date, category, parentID, duration=0):
        if due_date is None:
            self._due_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        else:
            self._due_date = due_date
        self._task_id = uuid.uuid4()
        self._task_category = category
        self._task_name = name

    def get_receipt(self):
        table = [
            ["Name", self._task_name],
            ["ID", self._task_id],
            ["Due date: ", self.get_due_date()],
        ]

        # todo: figure out task tree

        category = self._task_category

        lines = [
            f"{self._task_name.center(60)}",
            "=" * 60,
            "",
            f"{'Due:'.ljust(12)}{self.get_due_date()}",
            (
                f"\n{'Time:'.ljust(12)}{self._due_date.strftime("%H:%M")}\n"
                f"\n{'Category:'.ljust(12)}{category}\n"
                if category is not None
                else ""
            ),
            "-" * 60,
            "",
            f"{str(self._task_id)[:8]}",
            "",
        ]
        return lines

    def get_due_date(self):
        if self._due_date is None:
            return "No deadline"

        return self._due_date.strftime("%A, %d %B")
