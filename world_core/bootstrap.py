from world_core.world_space import WorldSpace
from world_core.world_grid import WorldGrid

from world_core.ledger import Ledger
from world_core.investigator_bot import InvestigatorBot

from world_core.observer_bot import ObserverBot
from world_core.walker_bot import WalkerBot
from world_core.scout_bot import ScoutBot
from world_core.surveyor_bot import SurveyorBot

from world_core.concierge_bot import ConciergeBot
from world_core.language_bot import LanguageBot
from world_core.manager_bot import ManagerBot
from world_core.reception_bot import ReceptionBot
from world_core.architect_bot import ArchitectBot
from world_core.builder_bot import BuilderBot

from world_core.profiles.neighbourhood_profile import NeighbourhoodProfile
from world_core.profiles.street_profile import StreetProfile
from world_core.profiles.person_profile import PersonProfile
from world_core.profiles.animal_profile import AnimalProfile

from world_core.profiles.park_profile import ParkProfile
from world_core.profiles.house_profile import HouseProfile


# ======================================================
# WORLD STATE
# ======================================================

class WorldState:
    def __init__(self, clock):
        self.clock = clock
        self.frame = 0

        # physical layers
        self.space = WorldSpace()
        self.grid = WorldGrid()
        self.places = {}

        # population (profiles, not agents)
        self.people = []
        self.animals = []

        # active agents
        self.agents = []
        self.scouts = []
        self.surveyor = None

        # cognition pipeline
        self.ledger = Ledger()
        self.investigator = InvestigatorBot()

        self.concierge = ConciergeBot()
        self.language = LanguageBot()
        self.manager = ManagerBot()
        self.reception = ReceptionBot()
        self.architect = ArchitectBot()
        self.builder = BuilderBot()

    # -----------------------------
    # Registration helpers
    # -----------------------------

    def add_place(self, place):
        self.places[place.name] = place
        self.grid.register(place)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_scout(self, scout):
        self.scouts.append(scout)

    def set_surveyor(self, surveyor):
        self.surveyor = surveyor

    # -----------------------------
    # WORLD TICK
    # -----------------------------

    def tick(self):
        self.frame += 1
        self.space.tick(self.frame)

        # 1️⃣ Physical agents act & observe
        for a in self.agents:
            if hasattr(a, "tick"):
                a.tick(self.clock)
            if hasattr(a, "observe"):
                a.observe(self)

        # 2️⃣ Scouts observe fields
        for s in self.scouts:
            s.observe(self)

        # 3️⃣ Surveyor maps geometry
        if self.surveyor:
            self.surveyor.observe(self)

        # 4️⃣ Collect snapshots
        snapshots = []

        for a in self.agents:
            if hasattr(a, "snapshot"):
                snapshots.append(a.snapshot())

        for s in self.scouts:
            if hasattr(s, "snapshot"):
                snapshots.append(s.snapshot())

        if self.surveyor and hasattr(self.surveyor, "snapshot"):
            snapshots.append(self.surveyor.snapshot())

        # 5️⃣ Investigator → Ledger
        for snap in snapshots:
            events = self.investigator.ingest_snapshot(self.frame, snap)
            for ev in events:
                self.ledger.ingest(ev)

        # 6️⃣ Concierge proposes meaning
        self.concierge.propose(self.ledger.tail(200))

        # 7️⃣ Language ingests proposals (FIXED)
        lang_events = self.language.ingest_proposals(
            self.concierge.proposals_tail
        )

        # 8️⃣ Language events → Ledger
        for le in lang_events:
            events = self.investigator.ingest_snapshot(self.frame, le)
            for ev in events:
                self.ledger.ingest(ev)

        # 9️⃣ Manager gate decision
        decision = self.manager.decide(self.ledger.snapshot())

        # 🔟 Promote approved symbols
        if decision.get("approve_language"):
            for p in self.concierge.proposals_tail:
                sym = p.get("symbol_candidate")
                if sym:
                    self.language.accept(sym)
                    self.reception.accept_symbol(sym)

        # 11️⃣ Reception indexes world knowledge
        self.reception.update(self)

        # 12️⃣ Architect & Builder
        self.architect.generate(self.reception.registry)
        self.builder.execute(decision, self.architect.plans_tail())


# ======================================================
# WORLD CONSTRUCTION
# ======================================================

def build_world(clock):
    world = WorldState(clock)

    # -----------------------------
    # Neighbourhood root
    # -----------------------------
    neighbourhood = NeighbourhoodProfile(
        name="Neighbourhood-1",
        position=(4800.0, 5100.0, 0.0),
        size_m=1200.0
    )
    world.add_place(neighbourhood)

    # -----------------------------
    # Street
    # -----------------------------
    street = StreetProfile(
        name="Main Street",
        position=(4700.0, 5050.0, 0.0),
        length_m=600.0,
        width_m=20.0
    )
    world.add_place(street)

    # -----------------------------
    # Park
    # -----------------------------
    park = ParkProfile(
        name="Central Park",
        position=(5000.0, 5200.0, 0.0),
        trees=20
    )
    world.add_place(park)

    # -----------------------------
    # Houses
    # -----------------------------
    house_a = HouseProfile(
        name="Family House",
        position=(4800.0, 5100.0, 0.0),
        footprint=(50, 50),
        floors=2
    )
    world.add_place(house_a)

    house_b = HouseProfile(
        name="Neighbour House 1",
        position=(4900.0, 5105.0, 0.0),
        footprint=(45, 45),
        floors=2
    )
    world.add_place(house_b)

    # -----------------------------
    # People (profiles)
    # -----------------------------
    world.people.extend([
        PersonProfile("Alex", 12, "Family House", (4805.0, 5110.0, 0.0)),
        PersonProfile("Maya", 11, "Neighbour House 1", (4905.0, 5110.0, 0.0)),
        PersonProfile("Sam", 13, "Neighbour House 1", (4910.0, 5108.0, 0.0)),
    ])

    # -----------------------------
    # Animals
    # -----------------------------
    world.animals.extend([
        AnimalProfile("Rex", "dog", "black", (4803.0, 5106.0, 0.0)),
        AnimalProfile("Luna", "cat", "white", (4908.0, 5112.0, 0.0)),
    ])

    # -----------------------------
    # Agents
    # -----------------------------
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    walker = WalkerBot(
        name="Walker-1",
        start_xyz=house_a.position,
        world=world,
        return_interval=15
    )
    world.add_agent(walker)

    # -----------------------------
    # Scouts
    # -----------------------------
    world.add_scout(ScoutBot(
        name="Scout-Sound",
        mode="sound",
        center_xyz=house_a.position,
        extent_m=30,
        resolution_m=2.0
    ))

    world.add_scout(ScoutBot(
        name="Scout-Light",
        mode="light",
        center_xyz=house_a.position,
        extent_m=30,
        resolution_m=2.0
    ))

    # -----------------------------
    # Surveyor
    # -----------------------------
    surveyor = SurveyorBot(
        name="Surveyor-1",
        center_xyz=house_a.position,
        extent_m=30.0,
        resolution_m=2.0,
        height_m=8.0
    )
    world.set_surveyor(surveyor)

    return world