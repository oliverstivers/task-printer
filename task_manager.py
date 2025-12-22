# task_manager.py
from task import Task
import datetime
import pickle
from treelib import Tree
import random

# Module-level variables (instead of class variables)
tasks: list[Task] = []
task_tag_map: dict[int, Task] = {}
used_ids: set[int] = set()


def create_default_tasks():
    """Create default tasks for testing"""
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


def get_task_map() -> dict[int, Task]:
    return task_tag_map


def save_all_task_files():
    """Save tasks, tag map, and categories to files"""
    with open("tasks.pkl", "wb") as f:
        pickle.dump(tasks, f)
    with open("tagmap.pkl", "wb") as f:
        pickle.dump(task_tag_map, f)
    with open("categories.pkl", "wb") as f:
        categories = get_task_categories()
        pickle.dump(categories, f)


def load_tasks_from_file():
    """Load tasks from pickle files or create defaults"""
    global tasks, task_tag_map, used_ids

    try:
        with open("tasks.pkl", "rb") as f:
            tasks = pickle.load(f)
            print("Loaded tasks from file")
        with open("tagmap.pkl", "rb") as f:
            task_tag_map = pickle.load(f)
            used_ids = set(task_tag_map.keys())
            print("Loaded tag map from file")
    except FileNotFoundError:
        print("No saved tasks found, creating default tasks")
        create_default_tasks()


def build_tree():
    """Build and display task tree"""
    tree = Tree()
    tree.create_node("Root", "root")
    for task in tasks:
        tree.create_node(
            task._task_name,
            task._task_id,
            parent=task._parent_id if task._parent_id is not None else "root",
        )
    tree.show()


def assign_tags():
    """Assign random tag IDs to TODO tasks"""
    for task in tasks:
        if task._status == Task.Status.TODO:
            id = random.randint(0, 300)
            if id not in used_ids:
                task_tag_map[id] = task
                task._tag_id = id
                used_ids.add(id)

    with open("tagmap.pkl", "wb") as f:
        pickle.dump(task_tag_map, f)


def relinquish_tag(id: int):
    """Remove a tag from the tag map"""
    task_tag_map.pop(id, None)
    used_ids.discard(id)


def get_task_categories() -> list[str]:
    """Get all unique task categories"""
    categories = set()
    for task in tasks:
        if task._task_category is not None:
            categories.add(task._task_category)
    return list(categories)


def fetch_gcal_tasks():
    """Fetch tasks from Google Calendar (TODO)"""
    pass


if __name__ == "__main__":
    load_tasks_from_file()
    if not task_tag_map:  # Check if empty, not None
        assign_tags()
    for task in tasks:
        print(f"tag id: {task._tag_id}")
        print("\n".join(task.get_receipt()))

    save_all_task_files()
