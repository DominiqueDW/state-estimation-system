import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np

class CameraObserver:

    def __init__(self, camera_index=0):

        self.cap = cv2.VideoCapture("data/Intersection.mp4")

        if not self.cap.isOpened():
            raise RuntimeError("Failed to open video file")
        
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.dt = 1/fps

        self.model = YOLO("yolov8n.pt")  # lightweight model
        self.tracker = sv.ByteTrack()

        import numpy as np

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

        self.H, _ = cv2.findHomography(self.image_points, self.world_points)
        self.H_inv = np.linalg.inv(self.H)

    def get_observations(self):

        ret, frame = self.cap.read()

        if not ret:
            return [], None

        results = self.model(frame, task="detect")[0]

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
            cy = float(y2)  # bottom of bounding box

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