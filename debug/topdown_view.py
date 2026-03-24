import cv2 # Computer Vision library
import numpy as np


class TopDownView:
    def __init__(self):

        self.width = 800
        self.height = 600

        self.scale = 80  # pixels per world unit
    
    def world_to_screen(self, position):
        x = int(position[0] * self.scale)
        y = int(position[1] * self.scale)

        # invert y so positive goes upward
        y = self.height - y

        return (x, y)

    def draw_zones(self, frame, zones):
        for zone in zones:

            pts = []

            for p in zone.polygon:
                pts.append(self.world_to_screen(p))

            pts = np.array(pts, np.int32)

            cv2.polylines(
                frame,
                [pts],
                isClosed=True,
                color=(255, 255, 255),
                thickness=2
            )

            label_pos = self.world_to_screen(zone.polygon[0])

            cv2.putText(
                frame,
                zone.zone_id,
                label_pos,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255,255,255),
                1
            )

    def draw_entities(self, frame, world):
        for entity in world.entities.values():

            pos = self.world_to_screen(entity.position)

            cv2.circle(
                frame,
                pos,
                6,
                (0,255,0),
                -1
            )

            cv2.putText(
                frame,
                f"E{entity.entity_id}",
                (pos[0]+5, pos[1]-5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,255,0),
                1
            )

    def draw_observations(self, frame, observations):
        for obs in observations:

            pos = self.world_to_screen(obs["position"])

            cv2.circle(
                frame,
                pos,
                5,
                (0,0,255),   # RED
                -1
            )

            cv2.putText(
                frame,
                f"T{obs['track_id']}",
                (pos[0]+5, pos[1]-5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0,0,255),
                1
            )
    
    def render(self, world, zones, observations):
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        self.draw_zones(frame, zones)

        self.draw_observations(frame, observations)

        self.draw_entities(frame, world)

        cv2.imshow("World View", frame)

        cv2.waitKey(1)