# Copyright (c) 2025 Oliver Stivers
# Licensed under the MIT License. See LICENSE file in the project root for full license text.

from task import Task
import datetime


task1 = Task("Do laundry", category="chores", due_date=None, parentID=None)

receipt = task1.get_receipt()
print("\n".join(receipt))
