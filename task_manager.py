# Copyright (c) 2025 Oliver Stivers
# Licensed under the MIT License. See LICENSE file in the project root for full license text.

from task import Task
import datetime
import pickle
from treelib import Tree
import random
import json
import os
import time
import scanner


class TaskManager:
    tasks: list[Task] = []
    task_tag_map: dict[int, Task] = {}
    used_ids = set()
    

    def create_default_tasks():
        # TODO: add way to create tasks from cli/user input
        task1 = Task("Do laundry", category="chores", due_date=None)
        task2 = Task(
            "essay project", category="esrm", due_date=datetime.date(2025, 11, 2)
        )
        task3 = Task(
            "plan essay", category="esrm", due_date=datetime.date(2025, 10, 30)
        )
        task4 = Task(
            "plan essay 2", category="esrm", due_date=datetime.date(2025, 10, 31)
        )
        task5 = Task(
            "read books", category="esrm", due_date=datetime.date(2025, 10, 30)
        )

        task2.add_child(task3)
        task2.add_child(task4)
        task3.add_child(task5)

        TaskManager.tasks.append(task1)
        TaskManager.tasks.append(task2)
        TaskManager.tasks.append(task3)
        TaskManager.tasks.append(task4)
        TaskManager.tasks.append(task5)

    def save_tasks_to_file(tasks):
        with open("tasks.pkl", "wb") as f:
            pickle.dump(tasks, f)

    def load_tasks_from_file():
        try:
            with open("tasks.pkl", "rb") as f:
                TaskManager.tasks = pickle.load(f)
                print("Loaded tasks from file")
        except FileNotFoundError:
            print("No saved tasks found, creating default tasks")
            TaskManager.create_default_tasks()

    def build_tree():
        tree = Tree()
        tree.create_node("Root", "root")
        for task in TaskManager.tasks:
            tree.create_node(
                task._task_name,
                task._task_id,
                parent=task._parent_id if task._parent_id is not None else "root",
            )

        tree.show()

    def assign_tags():
        for task in TaskManager.tasks:
            if task._status == Task.Status.TODO:
                id = random.randint(0, 300)
                if id not in TaskManager.used_ids:
                    TaskManager.task_tag_map[id] = task
                    task._tag_id = id
                    TaskManager.used_ids.add(id)

    def relinquish_tag(id: int):
        TaskManager.task_tag_map.pop(id, None)
        TaskManager.used_ids.discard(id)


if __name__ == "__main__":

    TaskManager.load_tasks_from_file()

    TaskManager.assign_tags()
    for id in TaskManager.used_ids:
        task: Task = TaskManager.task_tag_map[id]
        print(str(id) + "\n".join(task.get_receipt()))
        task.generate_image("/Users/oliverstivers/Pictures/tasks")

    TaskManager.save_tasks_to_file(TaskManager.tasks)

    while True:

        for detection in scanner.Scanner.detections:
            id = detection.tag_id
            print(f"Detected tag ID: {id}")

        time.sleep(1)
