# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.walker_bot import WalkerBot
from world_core.observer_bot import ObserverBot
from world_core.scout_bot import ScoutBot
from world_core.salience_investigator_bot import SalienceInvestigatorBot

from world_core.sound.sound_field import SoundField

from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile
from world_core.profiles.tv_profile import TVProfile


class WorldState:
    """
    World container.
    Reality exists first.
    Cognition is downstream.
    """

    def __init__(self, clock):
        self.clock = clock

        # Physical layers
        self.grid = WorldGrid()
        self.sound_field = SoundField()

        # World contents
        self.places = {}
        self.agents = []
        self.scouts = []

        # Accounting / memory layer
        self.salience_investigator = SalienceInvestigatorBot()

    # -------------------------------------------------
    # Registration
    # -------------------------------------------------

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

        # Register any sound sources the place exposes
        if hasattr(place, "sound_sources"):
            for src in place.sound_sources:
                self.sound_field.register(src)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_scout(self, scout):
        self.scouts.append(scout)

    # -------------------------------------------------
    # WORLD TICK — SINGLE SOURCE OF TRUTH
    # -------------------------------------------------

    def tick(self):
        """
        One world frame:
        Physics → perception → accounting
        """

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

        # 3️⃣ Scouts run missions
        for scout in list(self.scouts):
            scout.observe(self)

            if hasattr(scout, "snapshot"):
                snap = scout.snapshot()
                if isinstance(snap, dict) and "source" in snap:
                    self.salience_investigator.ingest(snap)

            if not scout.active:
                self.scouts.remove(scout)


# -------------------------------------------------
# WORLD CONSTRUCTION
# -------------------------------------------------

def build_world(clock):
    """
    Constructs the base world.
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

    # -------------------------
    # TV (sound-producing object)
    # -------------------------
    tv = TVProfile(
        name="Living Room TV",
        position=(4820.0, 5110.0, 0.0),
    )

    # Attach TV to house (room-level object)
    if hasattr(house, "add_object"):
        house.add_object("tv", tv)

    # Register TV sound
    if hasattr(tv, "sound"):
        world.sound_field.register(tv.sound)

    world.add_place(house)

    # -------------------------
    # Observer (GLOBAL PERCEPTION)
    # -------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    # -------------------------
    # Walker (PHYSICAL ACTOR)
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    # -------------------------
    # Initial Scout (LOCAL PROBE)
    # -------------------------
    scout = ScoutBot(
        name="Scout-sound-211",
        center_xyz=house.position,
        grid_size=16,
        resolution=1,
        max_frames=300,
    )
    world.add_scout(scout)

    return world