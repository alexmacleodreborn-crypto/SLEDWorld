# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.walker_bot import WalkerBot
from world_core.observer_bot import ObserverBot
from world_core.salience_investigator_bot import SalienceInvestigatorBot

from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile


class WorldState:
    """
    Container for the entire simulated world.
    Holds spatial grid, places, and agents.
    """

    def __init__(self, clock):
        self.clock = clock
        self.grid = WorldGrid()
        self.places: dict[str, object] = {}
        self.agents: list = []

        # Accounting layer
        self.salience_investigator = SalienceInvestigatorBot()

    # -----------------------------------------
    # Registration
    # -----------------------------------------

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    # -----------------------------------------
    # World tick
    # -----------------------------------------

    def tick(self):
        """
        Advances world agents.
        Observer → Investigator happens AFTER perception.
        """
        observer = None

        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)

            if agent.__class__.__name__ == "ObserverBot":
                observer = agent

        # -------------------------------------
        # Observer → Investigator (ACCOUNTING)
        # -------------------------------------
        if observer:
            snapshot = observer.export_snapshot()
            self.salience_investigator.ingest_observer_snapshot(snapshot)


def build_world(clock):
    """
    Constructs the base world with places and agents.
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
    # Observer (PERCEPTION)
    # -------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    # -------------------------
    # Walker (PHYSICAL)
    # -------------------------
    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    return world