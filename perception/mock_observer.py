# Simulates a detector

import random

class MockObserver:

    def get_observations(self):

        observations = []

        # simulate detection failure
        if random.random() < 0.4:
            return observations

        observations.append({
            "track_id": 1,
            "position": [
                2 + random.uniform(-0.5, 0.5),
                1 + random.uniform(-0.5, 0.5)
            ],
            "confidence": 0.9
        })

        observations.append({
            "track_id": 2,
            "position": [
                6 + random.uniform(-0.5, 0.5),
                4 + random.uniform(-0.5, 0.5)
            ],
            "confidence": 0.9
        })

        return observations