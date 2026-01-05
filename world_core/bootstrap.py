# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile
from world_core.agents.walker_bot import WalkerBot


class WorldState:
    """
    Container for the entire simulated world.
    Holds spatial grid, places, and agents.
    """

    def __init__(self):
        self.grid = WorldGrid()
        self.places = {}
        self.agents = []

    # -----------------------------------------
    # Registration
    # -----------------------------------------

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    # -----------------------------------------
    # World tick
    # -----------------------------------------

    def tick(self):
        """
        Advances all world agents.
        Safe even if no agents exist.
        """
        for agent in self.agents:
            agent.tick()


def build_world():
    """
    Constructs the base world with spatially located places
    and one moving agent.
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

    # -------------------------
    # Walker Agent
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        position=house.position,
    )

    # Walk from house to park
    walker.set_target(park.position)

    world.add_agent(walker)

    return world