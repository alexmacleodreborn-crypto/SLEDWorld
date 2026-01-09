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
    Cognition is downstream.
    """

    def __init__(self, clock):
        self.clock = clock
        self.grid = WorldGrid()

        self.places = {}
        self.agents = []

        # Perception / accounting
        self.salience_investigator = SalienceInvestigatorBot()

        # Ephemeral probes
        self.scouts = []

    # -----------------------------------------
    # Registration
    # -----------------------------------------

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_scout(self, scout):
        self.scouts.append(scout)

    # -----------------------------------------
    # WORLD TICK (single source of truth)
    # -----------------------------------------

    def tick(self):
        # 1️⃣ Physics + perception
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)

            if hasattr(agent, "observe"):
                agent.observe(self)

        # 2️⃣ Agent snapshots → investigator
        for agent in self.agents:
            if hasattr(agent, "snapshot"):
                snap = agent.snapshot()
                if isinstance(snap, dict) and "source" in snap:
                    self.salience_investigator.ingest(snap)

        # 3️⃣ Scouts (ephemeral)
        for scout in list(self.scouts):
            scout.observe(self)

            snap = scout.snapshot()
            if "source" in snap:
                self.salience_investigator.ingest(snap)

            if not scout.active:
                self.scouts.remove(scout)


# =================================================
# WORLD CONSTRUCTION
# =================================================

def build_world(clock):
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
    # Observer (perception)
    # -------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    # -------------------------
    # Walker (physical)
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    # -------------------------
    # Scout (sound + shape probe)
    # -------------------------
    scout = ScoutBot(
        name="Scout-sound-211",
        center_xyz=house.position,
        grid_size=16,
        resolution=1.0,
        max_frames=300,
    )
    world.add_scout(scout)

    return world