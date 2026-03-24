import json

class ObservationRecorder:
    def __init__(self, filename):
        self.filename = filename
        self.frames = []

    def record(self, observations):
        self.frames.append(observations)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.frames, f)