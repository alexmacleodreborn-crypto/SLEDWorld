"""
World bootstrap.

Creates the physical world container:
- clock
- places
- environment

NO agents are created here.
NO MotherBot import.
"""

from world_core.world_clock import WorldClock


class World:
    def __init__(self):
        self.clock = WorldClock(acceleration=60)

        # Physical places (empty shells for now)
        self.places = {
            "home": {},
            "park": {},
            "street": {},
        }

    def tick(self, real_seconds=1.0):
        self.clock.tick(real_seconds=real_seconds)


def build_world():
    """
    Returns a pure world object.
    Agents are attached elsewhere.
    """
    return World()