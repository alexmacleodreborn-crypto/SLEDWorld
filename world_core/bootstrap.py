# world_core/bootstrap.py

from world_core.world_grid import WorldGrid
from world_core.walker_bot import WalkerBot
from world_core.observer_bot import ObserverBot
from world_core.scout_bot import ScoutBot
from world_core.surveyor_bot import SurveyorBot

from world_core.architect_bot import ArchitectBot
from world_core.builder_bot import BuilderBot
from world_core.language_bot import LanguageBot
from world_core.salience_investigator_bot import SalienceInvestigatorBot

from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile


class WorldState:
    """
    World container.
    One authoritative frame:
      Physics -> Perception -> Survey -> Accounting/Promotion -> Scouts
    """

    def __init__(self, clock):
        self.clock = clock
        self.grid = WorldGrid()
        self.places = {}
        self.agents = []

        # Bots
        self.surveyor = None
        self.architect = ArchitectBot()
        self.builder = BuilderBot()
        self.language = LanguageBot()

        # Ledger
        self.ledger = SalienceInvestigatorBot()
        self.ledger.attach(architect=self.architect, builder=self.builder, language=self.language)

        # Scouts
        self.scouts = []

        # frame counter (world-local)
        self.frame = 0

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_scout(self, scout):
        self.scouts.append(scout)

    def set_surveyor(self, surveyor):
        self.surveyor = surveyor

    def tick(self):
        self.frame += 1

        # 1) advance time
        # (clock.tick is done in Streamlit; this uses clock.world_datetime)

        # 2) physics (agents with tick)
        for a in self.agents:
            if hasattr(a, "tick"):
                a.tick(self.clock)

        # 3) perception (agents with observe)
        for a in self.agents:
            if hasattr(a, "observe"):
                a.observe(self)

        # 4) survey (geometry)
        if self.surveyor is not None:
            self.surveyor.observe(self)

        # 5) scouts
        for s in list(self.scouts):
            s.observe(self)
            if not getattr(s, "active", True):
                self.scouts.remove(s)

        # 6) ingest snapshots into ledger
        for a in self.agents:
            if hasattr(a, "snapshot"):
                snap = a.snapshot()
                if isinstance(snap, dict) and "source" in snap:
                    self.ledger.ingest(snap)

        for s in self.scouts:
            if hasattr(s, "snapshot"):
                snap = s.snapshot()
                if isinstance(snap, dict) and "source" in snap:
                    self.ledger.ingest(snap)

        if self.surveyor is not None:
            ss = self.surveyor.snapshot()
            # store surveyor geometry summary separately (not in main ledger list)
            self.ledger.ingest_surveyor_snapshot(ss)

        # 7) promotion (BRICK/WALL/ROOM/TV + language tokens)
        self.ledger.promote()


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
    # Agents
    # -------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
    )
    world.add_agent(walker)

    # -------------------------
    # Surveyor anchored at house center (or living room center if found)
    # -------------------------
    center = house.position
    if hasattr(house, "rooms"):
        for r in house.rooms.values():
            if getattr(r, "room_type", "") == "living_room":
                # center of room bounds if available
                b = getattr(r, "bounds", None)
                if b:
                    (min_x, min_y, min_z), (max_x, max_y, max_z) = b
                    center = ((min_x+max_x)/2, (min_y+max_y)/2, (min_z+max_z)/2)
                break

    surveyor = SurveyorBot(
        name="Surveyor-1",
        center_xyz=center,
        extent_m=12.0,
        resolution_m=1.0,
        height_m=6.0,
    )
    world.set_surveyor(surveyor)

    # -------------------------
    # Scout: stake out living room if known
    # -------------------------
    living_room_name = None
    if hasattr(house, "rooms"):
        for r in house.rooms.values():
            if getattr(r, "room_type", "") == "living_room":
                living_room_name = getattr(r, "name", None)

    scout = ScoutBot(
        name="Scout-living-1",
        target_room_name=living_room_name,
        grid_size=32,
        resolution=1.0,
        max_frames=5000,
    )
    world.add_scout(scout)

    return world