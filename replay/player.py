import json

class ObservationPlayer:

    def __init__(self, filename):

        with open(filename, "r") as f:
            self.frames = json.load(f)

        self.index = 0

    def get_observations(self):

        if self.index >= len(self.frames):
            return []

        obs = self.frames[self.index]
        self.index += 1

        return obs