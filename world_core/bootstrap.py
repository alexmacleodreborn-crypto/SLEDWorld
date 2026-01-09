# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.walker_bot import WalkerBot
from world_core.observer_bot import ObserverBot
from world_core.scout_bot import ScoutBot
from world_core.salience_investigator_bot import SalienceInvestigatorBot

from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile


class WorldState:
    """
    World container.
    Reality exists first.
    All cognition is downstream.
    """

    def __init__(self, clock):
        self.clock = clock
        self.grid = WorldGrid()
        self.places = {}
        self.agents = []

        # Accounting / memory layer
        self.salience_investigator = SalienceInvestigatorBot()

        # Active scouts
        self.scouts = []

    # -----------------------------------------
    # Registration
    # -----------------------------------------

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    # -----------------------------------------
    # WORLD TICK (SINGLE SOURCE OF TRUTH)
    # -----------------------------------------

    def tick(self):
        """
        One world frame.
        Physics → perception → accounting.
        """

        # 1️⃣ Physics & perception
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)

            if hasattr(agent, "observe"):
                agent.observe(self)

        # 2️⃣ Feed ALL snapshots into investigator
        for agent in self.agents:
            if hasattr(agent, "snapshot"):
                snap = agent.snapshot()

                # Ensure snapshot declares its source
                if isinstance(snap, dict) and "source" in snap:
                    self.salience_investigator.ingest(snap)

        # 3️⃣ Scouts observe and report
        for scout in list(self.scouts):
            scout.observe(self)

            if hasattr(scout, "snapshot"):
                snap = scout.snapshot()
                if "source" in snap:
                    self.salience_investigator.ingest(snap)

            if not scout.active:
                self.scouts.remove(scout)


def build_world(clock):
    """
    Constructs the base world.
    """

    world = WorldState(clock)

    # -------------------------
    # Places
    # -------------------------
    park = ParkProfile(
        name="Central Park",
        position=(5000.0, 5200.0, 0.0),
        trees=20,
    )
    world.add_place(park)

    house = HouseProfile(
        name="Family House",
        position=(4800.0, 5100.0, 0.0),
        footprint=(50, 50),
        floors=2,
    )
    world.add_place(house)

    # -------------------------
    # Observer
    # -------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    # -------------------------
    # Walker
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    return world