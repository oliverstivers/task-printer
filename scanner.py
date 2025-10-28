from pupil_apriltags import Detector
import cv2

detector = Detector(families="tag36h11")


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

scanned_ids = []


while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detections = detector.detect(gray)
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
        if(scanned_ids.count(id) == 0):
            scanned_ids.append(id)
            print(f"Detected tag: {detection.tag_id}")

    cv2.imshow("Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
