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
    Perception, accounting, exploration are downstream.
    """

    def __init__(self, clock):
        self.clock = clock
        self.grid = WorldGrid()

        # Spatial entities
        self.places: dict[str, object] = {}

        # Agents (walker, observer, etc.)
        self.agents: list = []

        # Scouts (activated by salience)
        self.scouts: list = []

        # Accounting layer (Σ)
        self.salience_investigator = SalienceInvestigatorBot()

    # =================================================
    # REGISTRATION
    # =================================================

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_scout(self, scout):
        self.scouts.append(scout)

    # =================================================
    # WORLD TICK — SINGLE SOURCE OF TRUTH
    # =================================================

    def tick(self):
        """
        One world frame.

        Order is STRICT:
        1) Physics (movement, interaction)
        2) Perception (observer)
        3) Accounting (investigator)
        4) Exploration (scouts)
        """

        observer_snapshot = None

        # ---------------------------------------------
        # 1️⃣ Physics + perception
        # ---------------------------------------------
        for agent in self.agents:
            # Physical evolution
            if hasattr(agent, "tick"):
                agent.tick(self.clock)

            # Perceptual sampling
            if hasattr(agent, "observe"):
                agent.observe(self)

            # Capture observer output
            if agent.__class__.__name__ == "ObserverBot":
                observer_snapshot = agent.snapshot()

        # ---------------------------------------------
        # 2️⃣ Accounting (SALIENT MEMORY)
        # ---------------------------------------------
        if observer_snapshot:
            self.salience_investigator.ingest(observer_snapshot)

        # ---------------------------------------------
        # 3️⃣ Scout activation + observation
        # ---------------------------------------------
        if self.salience_investigator.frame_counter > 0:
            for scout in list(self.scouts):
                scout.active = True
                scout.observe(self)

                if not scout.active:
                    self.scouts.remove(scout)

    # =================================================
    # OBSERVER-FACING SNAPSHOT (DEBUG / STREAMLIT)
    # =================================================

    def snapshot(self):
        return {
            "places": {
                name: place.snapshot()
                for name, place in self.places.items()
            },
            "agents": [
                agent.snapshot()
                for agent in self.agents
                if hasattr(agent, "snapshot")
            ],
            "scouts": [
                scout.snapshot()
                for scout in self.scouts
                if hasattr(scout, "snapshot")
            ],
            "salience": self.salience_investigator.snapshot(),
        }


# =====================================================
# WORLD CONSTRUCTION
# =====================================================

def build_world(clock):
    """
    Constructs the base world with:
    - Places
    - Observer
    - Walker
    - Scout
    """

    world = WorldState(clock)

    # ---------------------------------------------
    # Places
    # ---------------------------------------------
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

    # ---------------------------------------------
    # Observer (GLOBAL PERCEPTION)
    # ---------------------------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    # ---------------------------------------------
    # Walker (PHYSICAL CAUSATION)
    # ---------------------------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    # ---------------------------------------------
    # Scout (LOCAL FIELD PROBE)
    # ---------------------------------------------
    scout = ScoutBot(
        name="Scout-vision-001",
        grid_size=16,
        resolution=1,
        max_frames=300,
    )
    world.add_scout(scout)

    return world