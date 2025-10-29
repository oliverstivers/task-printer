# Copyright (c) 2025 Oliver Stivers
# Licensed under the MIT License. See LICENSE file in the project root for full license text.

from task import Task
import datetime
import pickle



class TaskManager:
    tasks = []
    task1 = Task("Do laundry", category="chores", due_date=None, parentID=None)
    tasks.append(task1)

    def save_tasks_to_file(tasks):
        with open("tasks.pkl", "wb") as f:
            pickle.dump(tasks, f)


        
if __name__ == "__main__":
    with open("tasks.pkl", "rb") as f:
        tasks: list[Task] = pickle.load(f)

    for task in tasks:
        print("\n".join(task.get_receipt()))

        
