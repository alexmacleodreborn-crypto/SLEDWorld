# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.walker_bot import WalkerBot
from world_core.observer_bot import ObserverBot

from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile


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
        Observation is handled externally.
        Safe even if no agents exist.
        """
        for agent in self.agents:
            # Only agents with tick() are time-driven
            if hasattr(agent, "tick"):
                agent.tick(self.clock)


def build_world(clock):
    """
    Constructs the base world with places and agents.
    World-first. Agents inhabit, not control.
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
    # Observer Bot (PASSIVE, COGNITIVE)
    # -------------------------
    observer = ObserverBot(name="Observer-1")
world.add_agent(observer)

    # -------------------------
    # Walker Bot (AUTONOMOUS, PHYSICAL)
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    return world