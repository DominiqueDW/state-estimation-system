# Geometry should never depend on AI, it should only depend on math, coordinates, and tranformations

class Zone:
    def __init__(self, zone_id, polygon):

        self.zone_id = zone_id
        self.polygon = polygon

PARKING_ZONES = [

            Zone(
                "A1",
                [
                    (0, 0),
                    (3, 0),
                    (3, 2),
                    (0, 2)
                ]
            ),

            Zone(
                "A2",
                [
                    (4, 0),
                    (7, 0),
                    (7, 2),
                    (4, 2)
                ]
            )
        ]