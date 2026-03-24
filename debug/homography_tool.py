import cv2
import numpy as np

points = []


def click_event(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        print(f"Point added: {x}, {y}")


def select_points(video_path):

    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()

    if not ret:
        raise RuntimeError("Failed to read video")

    clone = frame.copy()

    cv2.namedWindow("Select Points")
    cv2.setMouseCallback("Select Points", click_event)

    while True:

        display = clone.copy()

        # draw selected points
        for pt in points:
            cv2.circle(display, tuple(pt), 5, (0, 0, 255), -1)

        # draw polygon if 4 points
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            cv2.polylines(display, [pts], True, (255, 0, 0), 2)

        cv2.imshow("Select Points", display)

        key = cv2.waitKey(1)

        if key == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

    return np.array(points, dtype=np.float32)