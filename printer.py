from task import Task
import queue

print_queue = queue.Queue()
completed_prints = []


# adds a task to the print queue call `process_print_queue() to send to printer`
def add_task_to_print_queue(task: Task):
    pass


# iterates through print queue and prints each task util queu is empty
def process_print_queue():
    # figure out how to interface with printer hardware
    pass


# reprints a task. can be used in case of a print error/for any reason you would need to reprint
def reprint_task(task: Task):
    pass


def generate_printable_image(task: Task):
    # TODO: port image stuff from Task.py
    pass
