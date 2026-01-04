"""
World bootstrap.
Creates a fully functional world independent of A7DO.
"""

from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot


def build_world(acceleration: int = 60):
    """
    Initialize and return core world objects.

    World exists independently of A7DO.
    """
    clock = WorldClock(acceleration=acceleration)

    mother = MotherBot(clock)

    world = {
        "clock": clock,
        "agents": {
            "mother": mother,
        },
    }

    return world