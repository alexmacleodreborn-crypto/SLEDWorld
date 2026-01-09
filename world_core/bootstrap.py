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
    Authoritative world container.

    Reality exists first.
    Cognition is downstream.
    """

    def __init__(self, clock):
        self.clock = clock
        self.frame = 0

        # Geometry
        self.grid = WorldGrid()
        self.places = {}

        # Agents
        self.agents = []

        # Ephemeral salience probes
        self.scouts = []

        # Meaning / memory ledger
        self.salience_investigator = SalienceInvestigatorBot()

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
        self.frame += 1

        # ------------------
        # Agents: physics + perception
        # ------------------
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)
            if hasattr(agent, "observe"):
                agent.observe(self)

            if hasattr(agent, "snapshot"):
                snap = agent.snapshot()
                if isinstance(snap, dict) and "source" in snap:
                    self.salience_investigator.ingest(snap, world=self)

        # ------------------
        # Scouts: salience probes
        # ------------------
        for scout in list(self.scouts):
            scout.observe(self)

            if hasattr(scout, "snapshot"):
                snap = scout.snapshot()
                if isinstance(snap, dict) and "source" in snap:
                    self.salience_investigator.ingest(snap, world=self)

            if not scout.active:
                self.scouts.remove(scout)


# ==================================================
# WORLD CONSTRUCTION (FROZEN)
# ==================================================

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
    # Observer (perception only)
    # -------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    # -------------------------
    # Walker (physical causality)
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
        return_interval=15,  # toggles TV regularly
    )
    world.add_agent(walker)

    # -------------------------
    # Scouts (salience channels)
    # -------------------------
    world.add_scout(
        ScoutBot(
            name="Scout-sound-1",
            focus="sound",
            target="tv",
            max_frames=300,
        )
    )

    world.add_scout(
        ScoutBot(
            name="Scout-light-1",
            focus="light",
            target="tv",
            max_frames=300,
        )
    )

    world.add_scout(
        ScoutBot(
            name="Scout-shape-1",
            focus="shape",
            target=None,
            max_frames=300,
        )
    )

    return world