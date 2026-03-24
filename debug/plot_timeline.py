import json
import matplotlib.pyplot as plt


with open("timeline.json", "r") as f:
    timeline = json.load(f)

entity_positions = {}

for t, frame in enumerate(timeline):

    for entity in frame["entities"]:

        entity_id = entity["id"]
        x = entity["position"][0]

        if entity_id not in entity_positions:
            entity_positions[entity_id] = []

        entity_positions[entity_id].append((t, x))

plt.figure()

for entity_id, values in entity_positions.items():

    times = [v[0] for v in values]
    xs = [v[1] for v in values]

    plt.plot(times, xs, label=f"Entity {entity_id}")

plt.xlabel("Frame")
plt.ylabel("X Position")
plt.title("Entity Position Over Time")
plt.legend()

zones = {}

for frame in timeline:

    for zone_id, state in frame["occupancy"].items():

        if zone_id not in zones:
            zones[zone_id] = []

        zones[zone_id].append(1 if state["occupied"] else 0)

plt.figure()

for zone_id, values in zones.items():

    plt.plot(values, label=zone_id)

plt.xlabel("Frame")
plt.ylabel("Occupied (1=True)")
plt.title("Zone Occupancy Over Time")
plt.legend()
plt.show()