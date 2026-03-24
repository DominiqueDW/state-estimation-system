from state.entity import EntityState
import numpy as np
import math

ASSOCIATION_GATE = 2.0
MAX_UNSEEN_TIME = 1.5

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

class WorldModel:
    def __init__(self):
        self.entities = {}

    def add_entity(self, entity_id, position, velocity=[0, 0]):
        entity = EntityState(entity_id)
        entity.initialize_state(position, velocity)
        self.entities[entity_id] = entity

    def tick(self, dt, observations=None):

        if observations is None:
            observations = []

        # predict all entities
        for entity in self.entities.values():
            entity.predict(dt)

        # track which entities were seen
        seen_ids = set()

        # process observations
        for obs in observations:

            track_id = obs["track_id"]

            if track_id in self.entities:
                entity = self.entities[track_id]
                entity.update_from_observation(obs["position"])
                seen_ids.add(track_id)

            else:
                # Lightweight ID stabilisation
                # try to match to existing entity before creating a new one
                matched_entity = None
                min_dist = float("inf")

                for entity in self.entities.values():
                    d = np.linalg.norm(np.array(entity.position) - np.array(obs["position"]))

                    if d < min_dist:
                        min_dist = d
                        matched_entity = entity

                if matched_entity is not None and min_dist < ASSOCIATION_GATE:
                    # reuse existing entity
                    matched_entity.update_from_observation(obs["position"])
                else:
                    # truly new object
                    self.add_entity(track_id, obs["position"])

        # remove stale entities
        to_remove = []

        for entity_id, entity in self.entities.items():
            if entity.time_since_seen > MAX_UNSEEN_TIME:
                to_remove.append(entity_id)

        for entity_id in to_remove:
            del self.entities[entity_id]

    


    
    
