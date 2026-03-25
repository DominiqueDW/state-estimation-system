import cv2 # Computer Vision library
import numpy as np


class TopDownView:
    def __init__(self):
        self.width = 750
        self.height = 800

        self.scale = 80  # pixels per world unit
    
    def world_to_screen(self, position):
        x = int(position[0] * self.scale)
        y = int(position[1] * self.scale)

        # invert y so positive goes upward
        y = self.height - y

        return (x, y)

    def draw_zones(self, frame, zones, occupancy=None):
        occ_map = {}
        if occupancy is not None:
            occ_map = {z["zone_id"]: z for z in occupancy}

        for zone in zones:
            state = occ_map.get(zone.zone_id, {})
            occupied = state.get("occupied", False)

            color = (0, 0, 255) if occupied else (0, 255, 0)

            pts = [self.world_to_screen(p) for p in zone.polygon]
            pts = np.array(pts, np.int32)

            cv2.polylines(frame, [pts], True, color, 2)

            label_pos = self.world_to_screen(zone.polygon[0])

            label = zone.zone_id
            if occupied:
                label += " (X)"

            cv2.putText(
                frame,
                label,
                label_pos,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
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
                (0,0,255),
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
    
    def render(self, frame, observations, world, zones, occupancy=None):
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        self.draw_zones(frame, zones, occupancy)
        self.draw_observations(frame, observations)
        self.draw_entities(frame, world)

        cv2.imshow("World View", frame)
        cv2.waitKey(1)