import cv2
from ultralytics import YOLO
import supervision as sv


class CameraObserver:

    def __init__(self, camera_index=0):

        self.cap = cv2.VideoCapture("data/Intersection.mp4")

        if not self.cap.isOpened():
            raise RuntimeError("Failed to open video file")
        
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.dt = 1/fps

        self.model = YOLO("yolov8n.pt")  # lightweight model
        self.tracker = sv.ByteTrack()

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

            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            observations.append({
                "track_id": int(track_id),
                "position": [cx / 100, cy / 100],
                "confidence": float(detections.confidence[i])
            })

        return observations, frame