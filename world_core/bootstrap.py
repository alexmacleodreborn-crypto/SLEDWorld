# world_core/bootstrap.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple

from world_core.world_grid import WorldGrid
from world_core.world_space import WorldSpace

from world_core.walker_bot import WalkerBot
from world_core.observer_bot import ObserverBot
from world_core.surveyor_bot import SurveyorBot
from world_core.scout_bot import ScoutBot

from world_core.salience_investigator_bot import SalienceInvestigatorBot
from world_core.architect_bot import ArchitectBot
from world_core.builder_bot import BuilderBot
from world_core.language_bot import LanguageBot

from world_core.profiles.neighbourhood_profile import NeighbourhoodProfile
from world_core.profiles.road_profile import RoadProfile
from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.hospital_profile import HospitalProfile
from world_core.profiles.house_profile import HouseProfile


@dataclass
class WorldState:
    clock: Any

    def __post_init__(self):
        self.grid = WorldGrid()
        self.space = WorldSpace()
        self.frame: int = 0

        self.places: Dict[str, object] = {}
        self.agents: List[object] = []

        # Focus probes
        self.scouts: List[ScoutBot] = []

        # World-creator pipeline
        self.ledger = SalienceInvestigatorBot()
        self.architect = ArchitectBot()
        self.builder = BuilderBot()
        self.language = LanguageBot()

        # Surveyor is global, always present
        self.surveyor = SurveyorBot(
            name="Surveyor-1",
            center_xyz=(0.0, 0.0, 0.0),
            extent_m=120.0,
            resolution_m=2.0,
            height_m=10.0,
            max_frames=999999,
        )

    # -------------------------
    # Registration
    # -------------------------
    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    def get_agent(self, class_name: str) -> Optional[object]:
        for a in self.agents:
            if a.__class__.__name__ == class_name:
                return a
        return None

    def deploy_scout(self, signal: str, center_xyz: Tuple[float, float, float], name: str, extent_m: float = 10.0, resolution_m: float = 1.0, max_frames: int = 50):
        scout = ScoutBot(
            name=name,
            signal=signal,
            center_xyz=center_xyz,
            extent_m=extent_m,
            resolution_m=resolution_m,
            max_frames=max_frames,
        )
        self.scouts.append(scout)
        return scout

    # -------------------------
    # World Tick
    # -------------------------
    def tick(self):
        """
        One frame:
          1) frame++ and world fields tick
          2) physics/actuation (walker)
          3) perception (observer)
          4) surveyor compile (geometry + aerial)
          5) scouts observe (if any)
          6) ledger ingest all snapshots
          7) architect proposes, builder validates
          8) ledger promotes, language binds words
        """
        self.frame += 1
        self.space.tick(self.frame)

        # 1) Agents act + perceive
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock, self)
        for agent in self.agents:
            if hasattr(agent, "observe"):
                agent.observe(self)

        # 2) Surveyor compiles geometry (global)
        # center is "world origin" of neighbourhood; keep stable
        self.surveyor.observe(self)

        # 3) Scouts
        for scout in list(self.scouts):
            scout.observe(self)
            if not scout.active:
                self.scouts.remove(scout)

        # 4) Ingest snapshots
        # Agents
        for agent in self.agents:
            if hasattr(agent, "snapshot"):
                snap = agent.snapshot()
                if isinstance(snap, dict) and snap.get("source"):
                    self.ledger.ingest(snap, world=self)

        # Surveyor
        self.ledger.ingest(self.surveyor.snapshot(), world=self)

        # Scouts
        for scout in self.scouts:
            self.ledger.ingest(scout.snapshot(), world=self)

        # 5) Architect/Builder cycle (ledger is truth)
        proposals = self.architect.propose(self.ledger)
        validations = self.builder.validate(proposals, self.ledger, self.surveyor)

        # Ledger promotions
        self.ledger.apply_structures(validations)

        # Language binding
        self.language.bind_from_symbols(self.ledger.symbols)


def build_world(clock):
    """
    Build a neighbourhood-scale world:
      - looping road "globe" (wrap)
      - one house with rooms and TV
      - park and hospital
    """
    world = WorldState(clock)

    # -------------------------
    # Neighbourhood origin
    # -------------------------
    neighbourhood = NeighbourhoodProfile(
        name="Neighbourhood-0",
        position=(0.0, 0.0, 0.0),
        size_xy=(240.0, 240.0),
        wrap=True,
    )
    world.add_place(neighbourhood)

    # -------------------------
    # Road loop (simple ring)
    # -------------------------
    # A coarse square loop around centre
    road_n = RoadProfile("Main St North", position=(-100.0, 80.0, 0.0), length=200, width=10)
    road_s = RoadProfile("Main St South", position=(-100.0, -80.0, 0.0), length=200, width=10)
    road_e = RoadProfile("Main St East", position=(80.0, -100.0, 0.0), length=200, width=10, orientation="vertical")
    road_w = RoadProfile("Main St West", position=(-80.0, -100.0, 0.0), length=200, width=10, orientation="vertical")
    for r in (road_n, road_s, road_e, road_w):
        world.add_place(r)

    # -------------------------
    # House (with living room TV)
    # -------------------------
    house = HouseProfile(
        name="Family House",
        position=(-30.0, 0.0, 0.0),
        footprint=(20.0, 14.0),
        floors=1,
    )
    world.add_place(house)

    # -------------------------
    # Park
    # -------------------------
    park = ParkProfile(
        name="Central Park",
        position=(40.0, 30.0, 0.0),
        size_xy=(60.0, 60.0),
        trees=20,
    )
    world.add_place(park)

    # -------------------------
    # Hospital
    # -------------------------
    hospital = HospitalProfile(
        name="Local Hospital",
        position=(50.0, -40.0, 0.0),
        footprint=(30.0, 20.0),
        floors=1,
    )
    world.add_place(hospital)

    # -------------------------
    # World bots (creators)
    # -------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world_bounds=neighbourhood.bounds,  # for wrap
        return_to_tv_every=15,
        speed_m_per_min=6.0,
    )
    world.add_agent(walker)

    # Set surveyor centre at neighbourhood centre
    world.surveyor.center_xyz = neighbourhood.center_xyz()

    return world