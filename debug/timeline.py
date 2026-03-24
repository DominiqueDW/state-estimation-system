import json

class TimelineRecorder:

    def __init__(self):
        self.data = []

    def record(self, world, occupancy):

        frame_data = {
            "entities": [],
            "occupancy": occupancy
        }

        for entity in world.entities.values():
            frame_data["entities"].append({
                "id": entity.entity_id,
                "position": entity.position,
                "velocity": entity.velocity
            })

        self.data.append(frame_data)

    def save(self, filename="timeline.json"):

        with open(filename, "w") as f:
            json.dump(self.data, f, indent=2)