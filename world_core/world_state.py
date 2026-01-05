from typing import Dict, List
from world_core.world_clock import WorldClock


class WorldState:
    """
    Root container for the entire physical world.

    Owns:
    - World clock
    - All places
    - All world objects
    - All agents (later)
    """

    def __init__(self, acceleration: float = 60.0):
        # ----------------------------------
        # TIME (authoritative)
        # ----------------------------------
        self.clock = WorldClock(acceleration=acceleration)

        # ----------------------------------
        # WORLD STRUCTURE
        # ----------------------------------
        self.places: Dict[str, object] = {}
        self.objects: List[object] = []

    # ----------------------------------
    # WORLD TICK
    # ----------------------------------

    def tick(self, real_seconds: float):
        """
        Advance the world by real_seconds.
        """
        self.clock.tick(real_seconds=real_seconds)

        # Tick all places
        for place in self.places.values():
            if hasattr(place, "tick"):
                place.tick(real_seconds)

        # Tick all world objects
        for obj in self.objects:
            if hasattr(obj, "tick"):
                obj.tick(real_seconds)

    # ----------------------------------
    # OBSERVER SNAPSHOT
    # ----------------------------------

    def snapshot(self):
        return {
            "time": self.clock.snapshot(),
            "places": {
                name: place.snapshot()
                for name, place in self.places.items()
                if hasattr(place, "snapshot")
            },
            "objects": [
                obj.snapshot()
                for obj in self.objects
                if hasattr(obj, "snapshot")
            ],
        }