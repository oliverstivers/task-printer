# Copyright (c) 2025 Oliver Stivers
# Licensed under the MIT License. See LICENSE file in the project root for full license text.


from task import Task
import queue

print_queue = queue.Queue()
completed_prints = []


# adds a task to the print queue call `process_print_queue() to send to printer`
def add_task_to_print_queue(task: Task):
    print_queue.put(task)


# iterates through print queue and prints each task util queu is empty
def process_print_queue():
    # figure out how to interface with printer hardware
    while not print_queue.empty():
        # print task
        task_to_print = print_queue.get()
        printable_image = task_to_print.gener
    pass


# reprints a task. can be used in case of a print error/for any reason you would need to reprint
def reprint_task(task: Task):
    pass


