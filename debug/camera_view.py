import cv2
import numpy as np

class CameraView:

    def render(self, frame, observations, world, image_points=None, H_inv=None):

        display = frame.copy()

        # draw homography region
        if image_points is not None:
            pts = image_points.astype(int)
            cv2.polylines(display, [pts], True, (255, 0, 0), 2)

        # draw detections (RED)
        for obs in observations:

            px, py = obs["pixel"]
            cv2.circle(display, (int(px), int(py)), 5, (0, 0, 255), -1)
        
        # draw entities (GREEN) using inverse homography
        if H_inv is not None:

            for entity in world.entities.values():

                wx, wy = entity.position

                world_point = np.array([[[wx, wy]]], dtype=np.float32)

                pixel_point = cv2.perspectiveTransform(world_point, H_inv)

                px = int(pixel_point[0][0][0])
                py = int(pixel_point[0][0][1])

                cv2.circle(display, (px, py), 4, (0, 255, 0), -1)

                cv2.putText(
                    display,
                    f"E{entity.entity_id}",
                    (px + 5, py - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1
                )
        
        cv2.imshow("Camera View", display)
        cv2.waitKey(1)