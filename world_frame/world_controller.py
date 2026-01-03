from world_frame.event_generator import EventGenerator

class WorldController:
    WORLD_NAME = "SLED World"

    def __init__(self):
        self.day = 0

        # minimal places for now (we will expand later)
        self.places = ["hospital", "car", "home"]

        self.generator = EventGenerator(seed=7)

        # Birth anchor is hospital
        self.birth_place = "hospital"
        self.home_place = "home"

    def snapshot(self):
        return {
            "world": self.WORLD_NAME,
            "day": self.day,
            "places": self.places,
            "birth_place": self.birth_place,
            "home_place": self.home_place,
        }

    # --- Anchors ---
    def birth_events(self):
        # Still one strong event, but we'll let the continuous stream do the richness
        return [{
            "place": self.birth_place,
            "intensity": 3.8,
            "pattern": "pressure-light-noise"
        }]

    def newborn_tick_events(self, place: str, tick_index: int, body_snapshot: dict):
        return self.generator.newborn_awake_stream(place, tick_index, body_snapshot)