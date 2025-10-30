# Copyright (c) 2025 Oliver Stivers
# Licensed under the MIT License. See LICENSE file in the project root for full license text.


import datetime
import uuid
from enum import Enum




# Each task will represent something i have to do
# can have subtasks, everything will either have a due date or a time that it will be done
# potentailly have some sort of distinction between tasks that are "reminders" (i.e. midterm on this day, essay)
# "reminders" can have subtasks and methods to generate
# we should keep track of a print time that controls when the task is printed, can be set explicitly or automatically
class Task:
    class Status(Enum):
        TODO = 0
        DOING = 1
        DONE = 3


    _due_date = None
    _duration = 0
    _task_id = None
    _print_time = None
    _task_name = None
    _task_category = ""
    _parent_id = None
    _child_ids = []
    _status: Status = Status.TODO



    def __init__(self, name, due_date: datetime.datetime | None, category, duration=0):
        if due_date is None:
            self._due_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        else:
            self._due_date = due_date
        self._task_id = uuid.uuid4()
        self._task_category = category
        self._task_name = name
        
   

    # TODO: figure out how to format actual printed image
    # make title a heading, bolded perhaps, etc.
    def get_receipt(self):

        # TODO: figure out task tree
        # tree should travel up to the top parent and display entire chain of tasks down to the furthest leaf
        # potentially look into anytree pip

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
    
    def add_child(self, child: Task):
        self._child_ids.append(child._task_id)
        child._parent_id = self._task_id

    def get_due_date(self):
        if self._due_date is None:
            return "No deadline"

        return self._due_date.strftime("%A, %d %B")
