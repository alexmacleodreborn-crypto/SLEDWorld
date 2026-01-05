# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile
from world_core.walker_bot import WalkerBot


class WorldState:
    """
    Container for the entire simulated world.
    Holds spatial grid, places, and agents.
    """

    def __init__(self, clock):
        self.clock = clock
        self.grid = WorldGrid()
        self.places: dict[str, object] = {}
        self.agents: list = []

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
        Advances all world agents using world time.
        """
        for agent in self.agents:
            agent.tick(self.clock)


def build_world(clock):
    """
    Constructs the base world with places and one physical walker.
    Pure world layer. No cognition.
    """

    world = WorldState(clock)

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
        footprint=(50, 50),
        floors=2,
    )
    world.add_place(house)

    # -------------------------
    # Walker Bot (PHYSICAL, XYZ-based)
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,  # ✅ correct anchor
        world=world,               # ✅ semantic resolution source
    )

    # Optional initial destination
    walker.set_target(park.position)

    world.add_agent(walker)

    return world