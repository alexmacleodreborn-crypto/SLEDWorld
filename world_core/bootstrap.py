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
    Physics -> perception -> accounting -> scouts
    """

    def __init__(self, clock):
        self.clock = clock
        self.grid = WorldGrid()
        self.places = {}
        self.agents = []

        self.salience_investigator = SalienceInvestigatorBot()
        self.scouts = []

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_scout(self, scout):
        self.scouts.append(scout)

    def tick(self):
        """
        One authoritative frame:
          1) physics (tick)
          2) perception (observe)
          3) accounting ingest (snapshots)
          4) scout observe + ingest
        """

        # 1) physics
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)

        # 2) perception
        for agent in self.agents:
            if hasattr(agent, "observe"):
                agent.observe(self)

        # 3) accounting ingest (agents)
        for agent in self.agents:
            if hasattr(agent, "snapshot"):
                try:
                    snap = agent.snapshot()
                except Exception:
                    continue
                if isinstance(snap, dict) and "source" in snap:
                    self.salience_investigator.ingest(snap)

        # 4) scouts
        for scout in list(self.scouts):
            scout.observe(self)
            ss = scout.snapshot()
            if isinstance(ss, dict) and "source" in ss:
                self.salience_investigator.ingest(ss)
            if not scout.active:
                self.scouts.remove(scout)


def build_world(clock):
    world = WorldState(clock)

    # Places
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

    # Agents
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    # Scout: stake out the living room (if known)
    # If your HouseProfile names the living room differently, set target_room_name accordingly.
    living_room_name = None
    if hasattr(house, "rooms"):
        for r in house.rooms.values():
            if getattr(r, "room_type", "") == "living_room":
                living_room_name = getattr(r, "name", None)

    scout = ScoutBot(
        name="Scout-sound-211",
        target_room_name=living_room_name,
        grid_size=32,
        resolution=1.0,
        max_frames=500,
    )
    world.add_scout(scout)

    return world