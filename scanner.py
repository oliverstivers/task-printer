# Copyright (c) 2025 Oliver Stivers
# Licensed under the MIT License. See LICENSE file in the project root for full license text.

from cv2.typing import MatLike
import task_manager
from pupil_apriltags import Detector, Detection
from task import Task
import cv2
import json
import os

from typing import Callable

currentID = -1
scanned_ids_file = "scanned_ids.json"
scanned_ids = []
detections: list[Detection] = []


def get_detections(frame) -> list[Detection]:
    detector = Detector(families="tag36h11")
    detections = detector.detect(frame)
    return detections


def update_tasks(frame):
    for detection in get_detections(frame):
        detection: Detection
        # TOOD: make sure that the frame width is correct
        task_manager.get_task_map().get(detection.tag_id)._status = detection_to_zone(  # type: ignore
            detection, 1280
        )


def detection_to_zone(detection: Detection, frame_width: int) -> Task.Status:
    corners = detection.corners.astype(int)
    x_coords = [int(corners[i][0]) for i in range(4)]
    avg_x = sum(x_coords) / len(x_coords)
    if avg_x < frame_width / 3:
        return Task.Status.TODO
    elif avg_x > frame_width / 3 and avg_x < frame_width / 3 * 2:
        return Task.Status.DOING
    else:
        return Task.Status.DONE


def detect():
    detector = Detector(families="tag36h11")

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print(
            "Error: Could not open camera. Please grant camera permissions in System Settings > Privacy & Security > Camera."
        )
        return

    while True:
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Error: Failed to capture frame from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detections: Detection = detector.detect(gray)
        cv2.line(frame, ((int(1280 / 3)), 0), ((int(1280 / 3)), 720), (255, 0, 0), 2)
        cv2.line(
            frame,
            ((int(1280 / 3 * 2)), 0),
            ((int(1280 / 3 * 2)), 720),
            (255, 0, 0),
            2,
        )
        for detection in detections:
            # Get corners and convert to integers
            corners = detection.corners.astype(int)

            # Draw box around the tag (connect all 4 corners)
            for i in range(4):
                pt1 = tuple(corners[i])
                pt2 = tuple(corners[(i + 1) % 4])
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            # Draw center point
            center = tuple(detection.center.astype(int))
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # Add tag ID text
            cv2.putText(
                frame,
                f"ID: {detection.tag_id}",
                (center[0] - 20, center[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2,
            )

            id = detection.tag_id

            task_status: Task.Status
            # print(f"id: {id}, corners: {corners}")
            # corner_x_coords = [int(corners[i][0]) for i in range(4)]
            # avg_x = sum(corner_x_coords) / 4
            # if avg_x < 1280 / 3:
            #     print("Tag is in the LEFT zone")
            # elif avg_x > 1280 / 3 * 2:
            #     print("Tag is in the RIGHT zone")
            # else:
            #     print("Tag is in the CENTER zone")

            if scanned_ids.count(id) == 0:
                scanned_ids.append(id)
                currentID = id

        cv2.imshow("Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
