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
    Reality exists first. Everything else observes or records.
    """

    def __init__(self, clock):
        self.clock = clock
        self.grid = WorldGrid()
        self.places = {}
        self.agents = []

        # Accounting / attention layer
        self.salience_investigator = SalienceInvestigatorBot()

        # Active scouts (spawned by investigator)
        self.scouts = []

    # -------------------------
    # Registration
    # -------------------------

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    # -------------------------
    # WORLD TICK (THE PIPELINE)
    # -------------------------

    def tick(self):
        """
        One world frame.
        """

        # 1️⃣ Physics
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)

        # 2️⃣ Perception
        for agent in self.agents:
            if hasattr(agent, "observe"):
                agent.observe(self)

        # 3️⃣ Accounting ingestion
        for agent in self.agents:
            if hasattr(agent, "export_event"):
                evt = agent.export_event()
                if evt:
                    self.salience_investigator.ingest_physical_event(evt)

            if hasattr(agent, "export_snapshot"):
                snap = agent.export_snapshot()
                if snap:
                    self.salience_investigator.ingest_observer_snapshot(snap)

        # 4️⃣ Investigator decides where to allocate attention
        new_scouts = self.salience_investigator.spawn_scouts_if_needed()

        for scout in new_scouts:
            self.scouts.append(scout)

        # 5️⃣ Scouts observe (depth + shape)
        for scout in list(self.scouts):
            scout.observe(self)

            if not scout.active:
                report = scout.export_report()
                self.salience_investigator.ingest_scout_report(report)
                self.scouts.remove(scout)


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
    # Walker
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    return world