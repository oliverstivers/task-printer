import datetime


# Each task will represent something i have to do
# can have subtasks, everything will either have a due date or a time that it will be done
# potentailly have some sort of distinction between tasks that are "reminders" (i.e. midterm on this day, essay)
# "reminders" can have subtasks and methods to generate
# we should keep track of a print time that controls when the task is printed, can be set explicitly or automatically
class Task:
    _due_date = None
    _duration = None
    _task_id = None
    _print_time = None

    def __init__(self, due_date):
        _due_date = due_date
    

    def getUnusedTaskId():
        
