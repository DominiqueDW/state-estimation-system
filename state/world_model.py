from state.entity import EntityState
from scipy.optimize import linear_sum_assignment
import numpy as np
import math

ASSOCIATION_GATE = 9.0
MAX_UNSEEN_TIME = 3.0

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

class WorldModel:
    def __init__(self):
        self.entities = {}
        self.next_id = 0

    def add_entity(self, position, velocity):
        entity = EntityState(self.next_id)
        entity.initialize_state(position, velocity)
        self.entities[self.next_id] = entity
        self.next_id += 1

    def tick(self, dt, observations=None):
        if observations is None:
            observations = []

        # update world every cycle
        for entity in self.entities.values():
            entity.predict(dt)

        entities = list(self.entities.values())

        # if no entities exist, add all observations as new entities
        if len(entities) == 0:
            for obs in observations:
                self.add_entity(obs["position"], [0, 0])
            return

        # Hungarian algorithm to associate entities with observations based on distance
        cost_matrix = []

        for entity in entities:
            row = []

            for obs in observations:
                row.append(entity.mahalanobis_distance(obs["position"]))
            cost_matrix.append(row)
        
        # row = entity, col = observation, value = distance between entity and observation
        cost_matrix = np.array(cost_matrix)

        # assign each entity to closest observation
        row_idx, col_idx = linear_sum_assignment(cost_matrix)

        # Track matched entities to avoid updating them multiple times
        matched_entities = set()
        matched_observations = set()
        
        # check association gate for each matched pair
        for r, c in zip(row_idx, col_idx):
            entity = entities[r]
            obs = observations[c]
            d = cost_matrix[r][c]

            if d <= ASSOCIATION_GATE:
                entity.update_from_observation(obs["position"])
                matched_entities.add(entity.entity_id) # for debugging purposes only
                matched_observations.add(c)
        
        # spawn new entities for unmatched observations
        for i, obs in enumerate(observations):

            if i not in matched_observations:
                self.add_entity(obs["position"], [0, 0])
        
        to_remove = []

        for entity_id, entity in self.entities.items():
            if entity.time_since_seen > MAX_UNSEEN_TIME:
                to_remove.append(entity_id)
        
        for entity_id in to_remove:
            del self.entities[entity_id]


    
    
