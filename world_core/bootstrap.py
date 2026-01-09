# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.world_space import WorldSpace

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
    """

    def __init__(self, clock):
        self.clock = clock
        self.grid = WorldGrid()
        self.places = {}
        self.agents = []

        self.space = WorldSpace(seed=211, frames_per_cycle=240)

        self.salience_investigator = SalienceInvestigatorBot()
        self.scouts = []
        self.surveyors = []

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_scout(self, scout):
        self.scouts.append(scout)

    def add_surveyor(self, surveyor):
        self.surveyors.append(surveyor)

    def tick(self):
        # Global fields first
        self.space.tick()

        # Agents
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)
            if hasattr(agent, "observe"):
                agent.observe(self)

        # Surveyors (geometry)
        for sv in list(self.surveyors):
            sv.observe(self)
            if not getattr(sv, "active", True):
                self.surveyors.remove(sv)

        # Scouts (field stakeouts)
        for sc in list(self.scouts):
            sc.observe(self)
            if not getattr(sc, "active", True):
                self.scouts.remove(sc)

        # Accounting ingest: world_space + everyone else
        self.salience_investigator.ingest(self.space.snapshot())

        for entity in [*self.agents, *self.surveyors, *self.scouts]:
            if hasattr(entity, "snapshot"):
                snap = entity.snapshot()
                if isinstance(snap, dict) and "source" in snap:
                    self.salience_investigator.ingest(snap)


def build_world(clock):
    world = WorldState(clock)

    # Places
    park = ParkProfile(name="Central Park", position=(5000.0, 5200.0, 0.0), trees=20)
    world.add_place(park)

    house = HouseProfile(name="Family House", position=(4800.0, 5100.0, 0.0), footprint=(50, 50), floors=2)
    world.add_place(house)

    # Agents
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    walker = WalkerBot(name="Walker-1", start_xyz=house.position, world=world)
    world.add_agent(walker)

    # Surveyor centered near house for now (you can later set to exact living room center)
    surveyor = SurveyorBot(
        name="Surveyor-house-slice",
        center_xyz=house.position,
        extent_m=20.0,
        resolution_m=1.0,
        max_frames=999999,
    )
    world.add_surveyor(surveyor)

    # Scout stakeout: living room TV fields (50 frames)
    scout = ScoutBot(
        name="Scout-tv-fields-211",
        target_room_type="living_room",
        target_object_key="tv",
        max_frames=50,
    )
    world.add_scout(scout)

    return world