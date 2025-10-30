# Copyright (c) 2025 Oliver Stivers
# Licensed under the MIT License. See LICENSE file in the project root for full license text.

from task import Task
import datetime
import pickle
from treelib import Tree
import random


class TaskManager:
    tasks: list[Task] = []
    task_tag_map: {int, Task} = {}
    used_ids = set()

    task1 = Task("Do laundry", category="chores", due_date=None)
    task2 = Task("essay project", category="esrm", due_date=datetime.date(2025, 11, 2))
    task3 = Task("plan essay", category="esrm", due_date=datetime.date(2025, 10, 30))
    task4 = Task("plan essay 2", category="esrm", due_date=datetime.date(2025, 10, 31))
    task5 = Task("read books", category="esrm", due_date=datetime.date(2025, 10, 30))
    task2.add_child(task3)
    task2.add_child(task4)
    task3.add_child(task5)

    tasks.append(task1)
    tasks.append(task2)
    tasks.append(task3)
    tasks.append(task4)
    tasks.append(task5)

    def save_tasks_to_file(tasks):
        with open("tasks.pkl", "wb") as f:
            pickle.dump(tasks, f)

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
            if(task._status == Task.Status.TODO):
                id = random.randint(0, 300)
                if(id not in TaskManager.used_ids):
                    TaskManager.task_tag_map[id] = task
                    TaskManager.used_ids.add(id)


if __name__ == "__main__":
    TaskManager.build_tree()
    TaskManager.assign_tags()
    for id in TaskManager.used_ids:
        task: Task = TaskManager.task_tag_map[id]
        print(str(id) + "\n".join(task.get_receipt()))
