# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.world_clock import WorldClock

# Physical / perceptual agents
from world_core.walker_bot import WalkerBot
from world_core.observer_bot import ObserverBot

# World survey & scouts
from world_core.surveyor_bot import SurveyorBot
from world_core.scout_bot import ScoutBot

# Cognitive / abstraction layer
from world_core.salience_investigator_bot import SalienceInvestigatorBot
from world_core.architect_bot import ArchitectBot
from world_core.builder_bot import BuilderBot
from world_core.language_bot import LanguageBot

# World profiles
from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile


class WorldState:
    """
    Authoritative world container.

    Order of truth:
    1. Geometry & physics
    2. Perception
    3. Ledger (accounting)
    4. Cognition / abstraction
    """

    def __init__(self, clock: WorldClock):
        self.clock = clock

        # Geometry
        self.grid = WorldGrid()
        self.places = {}
        self.agents = []

        # Central ledger (Sandy’s Law gate)
        self.ledger = SalienceInvestigatorBot()

        # Survey / scouts
        self.surveyor = None
        self.scouts = []

        # Cognitive layer (ghosts)
        self.architect = ArchitectBot()
        self.builder = BuilderBot()
        self.language = LanguageBot()

        # Frame counter (world-relative, NOT time)
        self.frame = 0

    # -------------------------------------------------
    # Registration
    # -------------------------------------------------

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_scout(self, scout):
        self.scouts.append(scout)

    # -------------------------------------------------
    # WORLD TICK (SINGLE SOURCE OF TRUTH)
    # -------------------------------------------------

    def tick(self):
        """
        One world frame.

        Physics → perception → ledger → cognition
        """
        self.frame += 1

        # -------------------------
        # 1) Physics & movement
        # -------------------------
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)

        # -------------------------
        # 2) Perception
        # -------------------------
        for agent in self.agents:
            if hasattr(agent, "observe"):
                agent.observe(self)

        # -------------------------
        # 3) Surveyor (geometry only)
        # -------------------------
        if self.surveyor:
            self.surveyor.observe(self)
            snap = self.surveyor.snapshot()
            self.ledger.ingest(snap, world=self)

        # -------------------------
        # 4) Scouts (light, sound, shape)
        # -------------------------
        for scout in list(self.scouts):
            scout.observe(self)
            snap = scout.snapshot()
            if snap:
                self.ledger.ingest(snap, world=self)

            if not scout.active:
                self.scouts.remove(scout)

        # -------------------------
        # 5) Agent snapshots → ledger
        # -------------------------
        for agent in self.agents:
            if hasattr(agent, "snapshot"):
                snap = agent.snapshot()
                if isinstance(snap, dict) and "source" in snap:
                    self.ledger.ingest(snap, world=self)

        # -------------------------
        # 6) Cognitive layer (READS ledger only)
        # -------------------------
        self.architect.review(self.ledger)
        self.ledger.ingest(self.architect.snapshot(), world=self)

        self.builder.review(self.ledger)
        self.ledger.ingest(self.builder.snapshot(), world=self)

        self.language.review(self.ledger)
        self.ledger.ingest(self.language.snapshot(), world=self)


# =====================================================
# WORLD CONSTRUCTION
# =====================================================

def build_world(clock: WorldClock) -> WorldState:
    """
    Builds the frozen pre-A7DO world.
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
    # Observer (perception only)
    # -------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    # -------------------------
    # Walker (physical interaction)
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    # -------------------------
    # Surveyor (geometry mapper)
    # -------------------------
    world.surveyor = SurveyorBot(
        name="Surveyor-1",
        center_xyz=house.position,
        extent_m=20.0,
        resolution_m=1.0,
        height_m=6.0,
        max_frames=500,
    )

    # -------------------------
    # Scouts (light & sound)
    # -------------------------
    scout_sound = ScoutBot(
        name="Scout-Sound",
        mode="sound",
        max_frames=300,
    )
    world.add_scout(scout_sound)

    scout_light = ScoutBot(
        name="Scout-Light",
        mode="light",
        max_frames=300,
    )
    world.add_scout(scout_light)

    return world