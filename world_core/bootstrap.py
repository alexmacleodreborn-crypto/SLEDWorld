# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile


class WorldState:
    """
    Container for the entire simulated world.
    Holds spatial grid and world places.
    """

    def __init__(self):
        self.grid = WorldGrid()
        self.places = {}

    def add_place(self, place):
        self.places[place.name] = place


def build_world():
    """
    Constructs the base world with spatially located places.
    No agents. No A7DO. Pure world state.
    """

    world = WorldState()

    # -------------------------
    # Park
    # -------------------------
    park = ParkProfile(
        name="Central Park",
        position=(5000.0, 5200.0, 0.0),
        trees=20,
    )
    world.add_place(park)

    # -------------------------
    # House
    # -------------------------
    house = HouseProfile(
        name="Family House",
        position=(4800.0, 5100.0, 0.0),
        floors=2,
        footprint=(50, 50),
    )
    world.add_place(house)

    return world