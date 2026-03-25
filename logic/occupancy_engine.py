import cv2
import numpy as np


def point_in_polygon(point, polygon):
    polygon_contour = np.array(polygon, dtype=np.int32)

    # determines position of a point relative to a contour
    # 1 = inside, -1 = outside, 0 = on edge
    return cv2.pointPolygonTest(polygon_contour, tuple(point), False) >= 0

class OccupancyEngine:

    def __init__(self):
        self.zone_states = {}  # zone_id -> state

    def update(self, world, zones, dt):
        results = []

        for zone in zones:

            # initialize if needed
            if zone.zone_id not in self.zone_states:
                self.zone_states[zone.zone_id] = {
                    "occupied": False,
                    "confidence": 0.0,
                    "vehicle_id": None
                }

            state = self.zone_states[zone.zone_id]

            # check if any entity is inside
            is_occupied_now = False
            vehicle_id = None

            for entity in world.entities.values():

                if point_in_polygon(entity.position, zone.polygon):
                    is_occupied_now = True
                    vehicle_id = entity.entity_id
                    break

            # update confidence
            if is_occupied_now:
                state["confidence"] += dt
            else:
                state["confidence"] -= dt

            # clamp
            state["confidence"] = max(0.0, min(2.0, state["confidence"]))

            # threshold
            if state["confidence"] > 1.0:
                state["occupied"] = True
            elif state["confidence"] < 0.5:
                state["occupied"] = False

            state["vehicle_id"] = vehicle_id

            results.append({
                "zone_id": zone.zone_id,
                "occupied": state["occupied"],
                "vehicle_id": vehicle_id,
                "confidence": state["confidence"]
            })

        return results