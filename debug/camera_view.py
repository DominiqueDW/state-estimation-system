import cv2

class CameraView:

    def render(self, frame, observations, world):

        display = frame.copy()

        # draw detections
        for obs in observations:

            x, y = obs["position"]

            # convert back to pixel space (reverse your scaling)
            px = int(x * 100)
            py = int(y * 100)

            cv2.circle(display, (px, py), 5, (0, 0, 255), -1)
        
        # draw entities
        for entity in world.entities.values():

            x, y = entity.position

            px = int(x * 100)
            py = int(y * 100)

            cv2.circle(display, (px, py), 6, (0, 255, 0), -1)

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