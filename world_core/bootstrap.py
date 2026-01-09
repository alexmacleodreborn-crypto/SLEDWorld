# world_core/bootstrap.py

from __future__ import annotations
from typing import List

from world_core.world_grid import WorldGrid
from world_core.world_clock import WorldClock
from world_core.world_space import WorldSpace

from world_core.salience_investigator_bot import SalienceInvestigatorBot
from world_core.observer_bot import ObserverBot
from world_core.walker_bot import WalkerBot
from world_core.surveyor_bot import SurveyorBot
from world_core.scout_bot import ScoutBot

from world_core.profiles.neighbourhood_profile import NeighbourhoodProfile
from world_core.profiles.road_profile import RoadProfile
from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.hospital_profile import HospitalProfile
from world_core.profiles.house_profile import HouseProfile


# ==================================================
# WORLD STATE (AUTHORITATIVE REALITY)
# ==================================================

class WorldState:
    """
    Stage-1 World Genesis container.

    - Reality exists first
    - Bots observe and act
    - Ledger compiles truth
    - No cognition here
    """

    def __init__(self, clock: WorldClock):
        self.clock = clock

        # Core world infrastructure
        self.grid = WorldGrid()
        self.space = WorldSpace()

        # Places and agents
        self.places = {}
        self.agents: List[object] = []

        # Ledger (single source of truth)
        self.ledger = SalienceInvestigatorBot()

    # ----------------------------------------------
    # REGISTRATION
    # ----------------------------------------------

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    # ----------------------------------------------
    # WORLD TICK (ONLY ENTRY POINT)
    # ----------------------------------------------

    def tick(self):
        """
        One frame of reality.

        Order is CRITICAL and now frozen:
        1. Physics / actuation
        2. Perception
        3. Snapshot ingestion
        4. World-space update
        """

        # 1️⃣ Physics & actions
        for agent in self.agents:
            if hasattr(agent, "tick"):
                agent.tick(self.clock)

        # 2️⃣ Perception
        for agent in self.agents:
            if hasattr(agent, "observe"):
                agent.observe(self)

        # 3️⃣ Snapshot ingestion (DEFENSIVE)
        for agent in self.agents:
            if hasattr(agent, "snapshot"):
                snap = agent.snapshot()
                if isinstance(snap, dict):
                    self.ledger.ingest(snap, world=self)

        # 4️⃣ World-space fields
        self.space.tick(self.clock.frame_counter)
        space_snap = self.space.snapshot()
        self.ledger.ingest(space_snap, world=self)


# ==================================================
# WORLD CONSTRUCTION
# ==================================================

def build_world(clock: WorldClock) -> WorldState:
    """
    Build the Stage-1 world.

    This defines the FULL environment:
    neighbourhood → streets → houses → park → hospital
    """

    world = WorldState(clock)

    # ------------------------------------------------
    # NEIGHBOURHOOD (CONTAINER)
    # ------------------------------------------------

    neighbourhood = NeighbourhoodProfile(
        name="Neighbourhood-1",
        position=(0.0, 0.0, 0.0),
        size_m=1000.0,   # wraparound globe scale
    )
    world.add_place(neighbourhood)

    # ------------------------------------------------
    # STREETS (WRAP AROUND)
    # ------------------------------------------------

    street = RoadProfile(
        name="Main Street",
        position=(0.0, 0.0, 0.0),
        length=800,
        width=12,
    )
    world.add_place(street)

    # ------------------------------------------------
    # PARK
    # ------------------------------------------------

    park = ParkProfile(
        name="Central Park",
        position=(200.0, 150.0, 0.0),
        trees=20,
    )
    world.add_place(park)

    # ------------------------------------------------
    # HOSPITAL
    # ------------------------------------------------

    hospital = HospitalProfile(
        name="General Hospital",
        position=(-200.0, -100.0, 0.0),
    )
    world.add_place(hospital)

    # ------------------------------------------------
    # HOUSE
    # ------------------------------------------------

    house = HouseProfile(
        name="Family House",
        position=(100.0, 50.0, 0.0),
    )
    world.add_place(house)

    # ------------------------------------------------
    # WORLD-CREATOR BOTS (INVISIBLE LATER)
    # ------------------------------------------------

    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house.position,
        world=world,
        return_interval=15,  # toggles TV every 15 frames
    )
    world.add_agent(walker)

    surveyor = SurveyorBot(
        name="Surveyor-1",
        center_xyz=house.position,
        extent_m=20.0,
        resolution_m=1.0,
        height_m=6.0,
    )
    world.add_agent(surveyor)

    # Example scout (sound)
    scout_sound = ScoutBot(
        name="Scout-sound-1",
        signal="sound",
        center_xyz=house.position,
        radius_m=6.0,
        max_frames=200,
    )
    world.add_agent(scout_sound)

    # Example scout (light)
    scout_light = ScoutBot(
        name="Scout-light-1",
        signal="light",
        center_xyz=house.position,
        radius_m=6.0,
        max_frames=200,
    )
    world.add_agent(scout_light)

    return world