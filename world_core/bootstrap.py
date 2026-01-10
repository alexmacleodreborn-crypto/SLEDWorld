from world_core.world_grid import WorldGrid
from world_core.world_space import WorldSpace
from world_core.salience_ledger import SalienceLedger
from world_core.manager_bot import ManagerBot

from world_core.observer_bot import ObserverBot
from world_core.walker_bot import WalkerBot
from world_core.scout_bot import ScoutBot
from world_core.surveyor_bot import SurveyorBot

from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile


class WorldState:
    """
    World-first container.
    Reality exists first; cognition is downstream.
    """

    def __init__(self, clock):
        self.clock = clock
        self.grid = WorldGrid()
        self.space = WorldSpace()              # ✅ fixes observer/world.space errors
        self.ledger = SalienceLedger()
        self.manager = ManagerBot()

        self.places = {}
        self.agents = []
        self.scouts = []
        self.surveyor = None

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_scout(self, scout):
        self.scouts.append(scout)

    def set_surveyor(self, surveyor):
        self.surveyor = surveyor

    def get_agent(self, cls_name: str):
        for a in self.agents:
            if a.__class__.__name__ == cls_name:
                return a
        return None

    def tick(self):
        """
        SINGLE SOURCE OF TRUTH:
        1) space/frame update
        2) physics (tick)
        3) perception (observe)
        4) ledger ingest
        5) manager approvals / gating
        6) scouts + surveyor ingest
        """
        # 1) advance world space
        self.space.tick()

        # 2) agents tick
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)

        # 3) agents observe
        for agent in self.agents:
            if hasattr(agent, "observe"):
                agent.observe(self)

        # 4) ingest snapshots (agents)
        for agent in self.agents:
            if hasattr(agent, "snapshot"):
                snap = agent.snapshot()
                self.ledger.ingest(snap, world=self)

        # 5) surveyor
        if self.surveyor:
            self.surveyor.observe(self)
            self.ledger.ingest(self.surveyor.snapshot(), world=self)

        # 6) scouts
        for scout in list(self.scouts):
            scout.observe(self)
            self.ledger.ingest(scout.snapshot(), world=self)
            if not getattr(scout, "active", True):
                self.scouts.remove(scout)

        # 7) manager gating & approvals
        self.manager.review(self.ledger, world=self)


def build_world(clock):
    world = WorldState(clock)

    # Places
    park = ParkProfile(name="Central Park", position=(5000.0, 5200.0, 0.0), trees=20)
    world.add_place(park)

    house = HouseProfile(
        name="Family House",
        position=(4800.0, 5100.0, 0.0),
        footprint=(50, 50),
        floors=2,
    )
    world.add_place(house)

    # Agents
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
        return_interval=15,   # toggles TV every 15 frames
    )
    world.add_agent(walker)

    # Scout (local squares) – sound+light grids
    scout = ScoutBot(
        name="Scout-sound-1",
        center_xyz=(house.position[0] + 10, house.position[1] + 10, house.position[2]),
        extent_m=18.0,
        resolution_m=2.0,
        max_frames=999999,
    )
    world.add_scout(scout)

    # Surveyor
    surveyor = SurveyorBot(
        name="Surveyor-1",
        center_xyz=(house.position[0] + 25, house.position[1] + 25, house.position[2]),
        extent_m=60.0,
        resolution_m=4.0,
        height_m=12.0,
        max_frames=999999,
    )
    world.set_surveyor(surveyor)

    return world