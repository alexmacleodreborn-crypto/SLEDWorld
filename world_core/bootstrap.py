# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile

class WorldState:
    def __init__(self):
        self.grid = WorldGrid()
        self.places = {}

    def add_place(self, place):
        self.places[place.name] = place


def build_world():
    world = WorldState()

    # Add places with real coordinates
    world.add_place(ParkProfile(
        name="Central Park",
        x=5000,
        y=5200,
        z=0
    ))

    world.add_place(HouseProfile(
        name="Family House",
        x=4800,
        y=5100,
        z=0
    ))

    return world