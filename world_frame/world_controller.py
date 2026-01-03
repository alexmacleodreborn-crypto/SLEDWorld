class WorldController:
    WORLD_NAME = "SLED World"

    def __init__(self):
        self.day = 0
        self.places = ["hospital", "car", "home"]

    def birth_events(self):
        return [{
            "place": "hospital",
            "intensity": 4.0,
            "pattern": "pressure-light-noise"
        }]

    def generate_events(self):
        return [{
            "place": "home",
            "intensity": 1.5,
            "pattern": "ambient-quiet"
        }]

    def snapshot(self):
        return {
            "world": self.WORLD_NAME,
            "day": self.day,
            "places": self.places
        }