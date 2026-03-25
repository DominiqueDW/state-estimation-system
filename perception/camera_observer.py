import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np

def point_in_image_polygon(point, polygon):
    polygon_np = np.array(polygon, dtype=np.int32)
    return cv2.pointPolygonTest(polygon_np, tuple(point), False) >= 0

class CameraObserver:

    def __init__(self):

        self.cap = cv2.VideoCapture("data/Intersection.mp4")

        if not self.cap.isOpened():
            raise RuntimeError("Failed to open video file")
        
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.dt = 1/fps

        self.model = YOLO("yolov8n.pt")  # lightweight model
        self.tracker = sv.ByteTrack()

        self.image_points = np.array([
            [ 569,  692], # bottom-left
            [1307,  603], # bottom-right
            [ 693,  286], # top-right
            [ 308,  301]  # top-left
        ], dtype=np.float32)

        self.world_points = np.array([
            [0, 0],
            [10, 0],
            [10, 20],
            [0, 20]
        ], dtype=np.float32)

        # transformation map
        self.H, _ = cv2.findHomography(self.image_points, self.world_points)
        self.H_inv = np.linalg.inv(self.H)

    def get_observations(self):

        ret, frame = self.cap.read()

        # ret = true if frame is read correctly
        if not ret:
            return [], None

        results = self.model(frame, task="detect", verbose=False)[0]

        detections = sv.Detections.from_ultralytics(results)

        # filter vehicles
        mask = (detections.class_id == 2) | (detections.class_id == 5) | (detections.class_id == 7)
        detections = detections[mask]

        # run tracker
        detections = self.tracker.update_with_detections(detections)

        observations = []

        for i in range(len(detections)):

            x1, y1, x2, y2 = detections.xyxy[i]
            track_id = detections.tracker_id[i]

            if track_id is None:
                continue
            
            # approximation of where the car touches the road
            cx = float((x1 + x2) / 2)
            cy = float(y2)

            # only note observations within predefined area
            if not point_in_image_polygon((cx, cy), self.image_points):
                continue

            # convert real coordinate to world coordinates
            point = np.array([[[cx, cy]]], dtype=np.float32)

            world_point = cv2.perspectiveTransform(point, self.H)

            wx = float(world_point[0][0][0])
            wy = float(world_point[0][0][1])

            observations.append({
                "track_id": int(track_id),
                "position": [wx, wy],
                "pixel": [cx, cy],
                "confidence": float(detections.confidence[i])
            })

        return observations, frame