from geometry.utils import point_in_polygon

class OccupancyEngine:
    def compute(self, world, zones):

        occupancy = {}

        for zone in zones:

            occupied = False
            vehicle_id = None

            for entity in world.entities.values():

                inside = point_in_polygon(
                    entity.position,
                    zone.polygon
                )

                if inside:
                    occupied = True
                    vehicle_id = entity.entity_id
                    break

            occupancy[zone.zone_id] = {
                "occupied": occupied,
                "vehicle_id": vehicle_id
            }

        return occupancy