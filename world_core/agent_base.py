import random

class Agent:
    """
    Fully formed world agent.
    Has language, needs, goals.
    """

    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.location = None

        # Physiology
        self.hunger = 0.0
        self.fatigue = 0.0

        # State
        self.awake = True
        self.rng = random.Random(hash(name) & 0xffff)

    def tick(self, clock):
        # Hunger & fatigue always evolve
        self.hunger = min(1.0, self.hunger + 0.01)
        self.fatigue = min(1.0, self.fatigue + 0.005)

        # Sleep if exhausted
        if self.fatigue > 0.9:
            self.awake = False
        if self.fatigue < 0.2:
            self.awake = True

    def speak(self, text):
        return {
            "speaker": self.name,
            "text": text,
            "location": self.location.name if self.location else None,
        }

    def snapshot(self):
        return {
            "name": self.name,
            "role": self.role,
            "location": self.location.name if self.location else None,
            "hunger": round(self.hunger, 2),
            "fatigue": round(self.fatigue, 2),
            "awake": self.awake,
        }