from world_core.world_space import WorldSpace
from world_core.world_grid import WorldGrid

from world_core.ledger import Ledger
from world_core.investigator_bot import InvestigatorBot

from world_core.observer_bot import ObserverBot
from world_core.walker_bot import WalkerBot
from world_core.scout_bot import ScoutBot
from world_core.surveyor_bot import SurveyorBot

from world_core.manager_bot import ManagerBot
from world_core.concierge_bot import ConciergeBot
from world_core.language_bot import LanguageBot
from world_core.reception_bot import ReceptionBot
from world_core.architect_bot import ArchitectBot
from world_core.builder_bot import BuilderBot

from world_core.profiles.neighbourhood_profile import NeighbourhoodProfile
from world_core.profiles.street_profile import StreetProfile
from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile
from world_core.profiles.person_profile import PersonProfile
from world_core.profiles.animal_profile import AnimalProfile


class WorldState:
    """
    One source of truth.
    Everything exists, but downstream layers are GATED.
    """

    def __init__(self, clock):
        self.clock = clock
        self.frame = 0

        self.space = WorldSpace()
        self.grid = WorldGrid()
        self.places = {}

        # profiles (held behind manager approvals)
        self.people = []
        self.animals = []

        # agents/sensors
        self.agents = []
        self.scouts = []
        self.surveyor = None

        # pipeline
        self.ledger = Ledger()
        self.investigator = InvestigatorBot()

        self.manager = ManagerBot()
        self.concierge = ConciergeBot()
        self.language = LanguageBot()
        self.reception = ReceptionBot()
        self.architect = ArchitectBot()
        self.builder = BuilderBot()

        # latest grids for UI
        self._latest_sensor_grids = {"sound": None, "light": None}

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_scout(self, scout):
        self.scouts.append(scout)

    def set_surveyor(self, surveyor):
        self.surveyor = surveyor

    def get_latest_sensor_grid(self, mode: str):
        return self._latest_sensor_grids.get(mode)

    def tick(self):
        # frame + world space
        self.frame += 1
        self.space.tick(self.frame)

        # 1) physics + perception
        for a in self.agents:
            if hasattr(a, "tick"):
                a.tick(self.clock)
            if hasattr(a, "observe"):
                a.observe(self)

        for s in self.scouts:
            s.observe(self)
            # cache for UI (grid is numpy array)
            snap = s.snapshot()
            if snap.get("mode") in self._latest_sensor_grids and "grid" in snap:
                self._latest_sensor_grids[snap["mode"]] = snap["grid"]

        if self.surveyor:
            self.surveyor.observe(self)

        # 2) snapshots -> investigator -> ledger events
        snaps = []
        for a in self.agents:
            if hasattr(a, "snapshot"):
                snaps.append(a.snapshot())

        for s in self.scouts:
            snaps.append(s.snapshot())

        if self.surveyor and hasattr(self.surveyor, "snapshot"):
            snaps.append(self.surveyor.snapshot())

        for snap in snaps:
            events = self.investigator.ingest_snapshot(self.frame, snap)
            for ev in events:
                self.ledger.ingest(ev)

        # 3) recompute Sandy gates (authoritative)
        self.ledger.recompute_gates()

        gates = self.ledger.gates_snapshot()
        mgr = self.manager

        # 4) downstream layers (exist, but dormant until gates + approvals)
        if gates["object_stable"]:
            self.concierge.propose(self.ledger.tail(200))

        if gates["symbol_ready"]:
            lang_events = self.language.ingest_proposals(self.concierge.proposals_tail())
            for le in lang_events:
                for ev in self.investigator.ingest_snapshot(self.frame, le):
                    self.ledger.ingest(ev)
            self.ledger.recompute_gates()

        if mgr.approved("neighbourhood"):
            # allow the world index to include neighbourhood-level registry
            pass

        if mgr.approved("population"):
            # allow people/animals into reception registry
            pass

        if gates["structure_stable"] and mgr.approved("architect"):
            self.reception.update(self)
            self.architect.generate(self.reception.registry)

        if mgr.approved("builder") and mgr.approved("architect"):
            self.builder.execute(self.architect.plans_tail(), world=self)


def build_world(clock):
    world = WorldState(clock)

    # ------------------------------------------------
    # Places (always exist)
    # ------------------------------------------------
    neighbourhood = NeighbourhoodProfile(name="Neighbourhood-1", position=(4800.0, 5100.0, 0.0), size_m=1200.0)
    world.add_place(neighbourhood)

    street = StreetProfile(name="Main Street", position=(4700.0, 5050.0, 0.0), length_m=600.0, width_m=20.0)
    world.add_place(street)

    park = ParkProfile(name="Central Park", position=(5000.0, 5200.0, 0.0), trees=20)
    world.add_place(park)

    house_a = HouseProfile(name="Family House", position=(4800.0, 5100.0, 0.0), footprint=(50, 50), floors=2)
    world.add_place(house_a)

    house_b = HouseProfile(name="Neighbour House 1", position=(4900.0, 5105.0, 0.0), footprint=(45, 45), floors=2)
    world.add_place(house_b)

    # ------------------------------------------------
    # Profiles (exist, but held behind manager approval for reception/indexing)
    # ------------------------------------------------
    world.people.append(PersonProfile(name="Alex", age=12, home_name="Family House", position_xyz=(4805.0, 5110.0, 0.0)))
    world.people.append(PersonProfile(name="Maya", age=11, home_name="Neighbour House 1", position_xyz=(4905.0, 5110.0, 0.0)))

    world.animals.append(AnimalProfile(name="Rex", species="dog", color="black", position_xyz=(4803.0, 5106.0, 0.0)))
    world.animals.append(AnimalProfile(name="Luna", species="cat", color="white", position_xyz=(4908.0, 5112.0, 0.0)))

    # ------------------------------------------------
    # Agents (always active)
    # ------------------------------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house_a.position,
        world=world,
        return_interval=15,  # toggles TV every 15 frames
    )
    world.add_agent(walker)

    # ------------------------------------------------
    # Scouts (always active)
    # ------------------------------------------------
    world.add_scout(ScoutBot(name="Scout-Sound", mode="sound", center_xyz=house_a.position, extent_m=40, resolution_m=2.0))
    world.add_scout(ScoutBot(name="Scout-Light", mode="light", center_xyz=house_a.position, extent_m=40, resolution_m=2.0))

    # ------------------------------------------------
    # Surveyor (always active)
    # ------------------------------------------------
    world.set_surveyor(SurveyorBot(name="Surveyor-1", center_xyz=house_a.position, extent_m=40.0, resolution_m=2.0, height_m=8.0))

    return world