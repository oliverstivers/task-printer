# Copyright (c) 2025 Oliver Stivers
# Licensed under the MIT License. See LICENSE file in the project root for full license text.


from __future__ import annotations
import datetime
import uuid
import task_manager
from enum import Enum
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moms_apriltag import TagGenerator2


# Each task will represent something i have to do
# can have subtasks, everything will either have a due date or a time that it will be done
# potentailly have some sort of distinction between tasks that are "reminders" (i.e. midterm on this day, essay)
# "reminders" can have subtasks and methods to generate
# we should keep track of a print time that controls when the task is printed, can be set explicitly or automatically
class Task:
    class Status(Enum):
        TODO = "TODO"
        DOING = "DOING"
        DONE = "DONE"

    _due_date = None
    _recurrence = None
    _duration = 0
    _task_id = None
    _print_time = None
    _task_name = None
    _task_category = ""
    _parent_id = None
    _child_ids = []
    _tag_id: int = -1
    _status: Status = Status.TODO

    _outdated = False

    def __init__(
        self,
        name,
        due_date: datetime.datetime | None,
        category,
        duration=0,
        recurrence=None,
    ):
        if due_date is None:
            self._due_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        else:
            self._due_date = due_date
        self._print_time = self._due_date + datetime.timedelta(
            minutes=5
        )  # print 5 minutes after due date by default
        self._task_id = uuid.uuid4()
        self._duration = duration
        self._task_category = category
        self._task_name = name
        self._recurrence = recurrence

        self._printed_fields = [
            self._task_name,
            self._due_date,
            self._recurrence,
            self._duration,
            self._task_id,
            self._task_category,
            self._tag_id,
        ]

    # TODO: figure out how to format actual printed image
    # make title a heading, bolded perhaps, etc.
    def generate_image(self, path="") -> Image.Image:
        img = Image.new("RGB", (384, 600), "white")  # 384px = thermal printer width
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Courier", 24)
        smaller_font = ImageFont.truetype("Courier", 16)

        bbox = draw.textbbox((0, 0), self._task_name, font=font)
        text_width = bbox[2] - bbox[0]
        x_centered = (img.width - text_width) // 2
        (draw.text((x_centered, 20), f"{self._task_name}\n", fill="black", font=font),)

        draw.line([(20, 60), (364, 60)], fill="black", width=2)

        draw.text(
            (35, 80),
            f"{'*'.ljust(4)}{'Due: '}{self.get_due_date()}",
            fill="black",
            font=smaller_font,
        )
        if self._task_category is not None:
            draw.text(
                (35, 110),
                f"{'*'.ljust(4)}{'Category: ' + self._task_category}\n",
                fill="black",
                font=smaller_font,
            )

        draw.line([(20, 150), (364, 150)], fill="black", width=2)

        if self._tag_id >= 0:
            tg = TagGenerator2("tag36h11")
            tag_array = tg.generate(self._tag_id)
            tag = Image.fromarray(tag_array)

            tag_size = 150

            tag = tag.resize((tag_size, tag_size), Image.Resampling.NEAREST)

            x_centered = (384 - tag_size) // 2

            img.paste(tag, (x_centered, 200))

            # draw centered text "TAG ID = self._tag_id" (obviously get the actual id) under the tag
            tag_text = f"TAG ID: {self._tag_id}"
            tag_text_bbox = draw.textbbox((0, 0), tag_text, font=smaller_font)
            tag_text_width = tag_text_bbox[2] - tag_text_bbox[0]
            tag_text_x = (img.width - tag_text_width) // 2
            tag_text_y = 200 + tag_size + 10  # 10px margin below tag
            draw.text(
                (tag_text_x, tag_text_y), tag_text, fill="black", font=smaller_font
            )

        img.save(f"{path}/task_{str(self._task_id)[:8]}.png")
        return img

    def set_task_staus(self, status: Task.Status):
        if status == Task.Status.DONE:
            task_manager.relinquish_tag(self._tag_id)
        self._status = status

    def get_receipt(self):
        # TODO: figure out task tree
        # tree should travel up to the top parent and display entire chain of tasks down to the furthest leaf
        # potentially look into anytree pip

        category = self._task_category

        lines = [
            f"{self._task_name.center(60)}",
            "=" * 60,
            "",
            f"{'Due:'.ljust(12)}{self.get_due_date()}\n",
            f"{'Status:'.ljust(12)}{str(self._status.value)}",
            (
                f"\n{'Time:'.ljust(12)}{self._due_date.strftime('%H:%M')}\n"
                f"\n{'Category:'.ljust(12)}{category}\n"
                if category is not None
                else ""
            ),
            f"{'Apriltag ID: '.ljust(12)}{str(self._tag_id)}"
            if self._tag_id >= 0
            else "",
            "-" * 60,
            "",
            f"{str(self._task_id)[:8]}",
            "",
        ]
        return lines

    def add_child(self, child: Task):
        self._child_ids.append(child._task_id)
        child._parent_id = self._task_id

    def get_parent_task(self):
        return self._parent_id

    def get_children(self):
        return self._child_ids

    # updates the field in the task it's called on to contain
    def update_task(self, new_task: Task):
        # if the task has been printed, we also track that this task is out of date
        if self._print_time is not None:
            self._outdated = True
        self.__dict__.update(new_task.__dict__)

    def get_due_date(self):
        if self._due_date is None:
            return "No deadline"

        return self._due_date.strftime("%A, %d %B")
