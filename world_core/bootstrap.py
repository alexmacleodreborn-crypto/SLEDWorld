# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.walker_bot import WalkerBot
from world_core.observer_bot import ObserverBot
from world_core.scout_bot import ScoutBot
from world_core.surveyor_bot import SurveyorBot
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

        self.salience_investigator = SalienceInvestigatorBot()
        self.scouts = []
        self.surveyors = []

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

    def add_surveyor(self, surveyor):
        self.surveyors.append(surveyor)

    # -----------------------------------------
    # World tick
    # -----------------------------------------

    def tick(self):
        # 1️⃣ Agents: physics + perception
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)

            if hasattr(agent, "observe"):
                agent.observe(self)

        # 2️⃣ Surveyors (geometry)
        for surveyor in list(self.surveyors):
            surveyor.observe(self)
            if not surveyor.active:
                self.surveyors.remove(surveyor)

        # 3️⃣ Scouts (field stakeouts)
        for scout in list(self.scouts):
            scout.observe(self)
            if not scout.active:
                self.scouts.remove(scout)

        # 4️⃣ Accounting (ONLY snapshots)
        for entity in [*self.agents, *self.surveyors, *self.scouts]:
            if hasattr(entity, "snapshot"):
                snap = entity.snapshot()
                if isinstance(snap, dict) and "source" in snap:
                    self.salience_investigator.ingest(snap)


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
    # Observer
    # -------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    # -------------------------
    # Walker (physical only)
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    # -------------------------
    # Surveyor (geometry)
    # -------------------------
    surveyor = SurveyorBot(
        name="Surveyor-living-room",
        center_xyz=house.position,
        extent_m=6.0,
        resolution_m=0.5,
        max_frames=50,
    )
    world.add_surveyor(surveyor)

    return world