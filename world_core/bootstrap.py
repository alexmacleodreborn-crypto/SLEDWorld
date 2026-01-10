# world_core/bootstrap.py

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


class WorldState:
    def __init__(self, clock):
        self.clock = clock
        self.frame = 0

        self.space = WorldSpace()
        self.grid = WorldGrid()
        self.places = {}

        # population layer (profiles, not agents)
        self.people = []
        self.animals = []

        # agents
        self.agents = []
        self.scouts = []
        self.surveyor = None

        # pipeline
        self.ledger = Ledger()
        self.investigator = InvestigatorBot()

        self.concierge = ConciergeBot()
        self.language = LanguageBot()
        self.manager = ManagerBot()
        self.reception = ReceptionBot()
        self.architect = ArchitectBot()
        self.builder = BuilderBot()

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
        self.space.tick(self.frame)

        # 1) act/observe
        for a in self.agents:
            if hasattr(a, "tick"):
                a.tick(self.clock)
            if hasattr(a, "observe"):
                a.observe(self)

        for s in self.scouts:
            s.observe(self)

        if self.surveyor:
            self.surveyor.observe(self)

        # 2) investigator normalises snapshots -> ledger events
        snaps = []
        for a in self.agents:
            if hasattr(a, "snapshot"):
                snaps.append(a.snapshot())
        for s in self.scouts:
            snaps.append(s.snapshot())
        if self.surveyor and hasattr(self.surveyor, "snapshot"):
            snaps.append(self.surveyor.snapshot())

        for snap in snaps:
            for ev in self.investigator.ingest_snapshot(self.frame, snap):
                self.ledger.ingest(ev)

        # 3) concierge proposes
        self.concierge.propose(self.ledger.tail(200))

        # 4) language emits symbol candidates
        lang_events = self.language.ingest_proposals(self.concierge.proposals_tail())

        # 5) language events back into ledger
        for le in lang_events:
            # wrap as a ledger event via investigator
            for ev in self.investigator.ingest_snapshot(self.frame, le):
                self.ledger.ingest(ev)

        # 6) manager decides based on ledger gates
        decision = self.manager.decide(self.ledger.snapshot())

        # 7) promote accepted symbols into reception if approved
        if decision.get("approve_language"):
            for p in self.concierge.proposals_tail():
                sym = p.get("symbol_candidate")
                if sym:
                    self.language.accept(sym)
                    self.reception.accept_symbol(sym)

        # 8) reception indexes world
        self.reception.update(self)

        # 9) architect/builder
        self.architect.generate(self.reception.registry)
        self.builder.execute(decision, self.architect.plans_tail())


def build_world(clock):
    world = WorldState(clock)

    # Neighbourhood root
    neighbourhood = NeighbourhoodProfile(name="Neighbourhood-1", position=(4800.0, 5100.0, 0.0), size_m=1200.0)
    world.add_place(neighbourhood)

    # Street
    street = StreetProfile(name="Main Street", position=(4700.0, 5050.0, 0.0), length_m=600.0, width_m=20.0)
    world.add_place(street)

    # Park
    park = ParkProfile(name="Central Park", position=(5000.0, 5200.0, 0.0), trees=20)
    world.add_place(park)

    # Houses
    house_a = HouseProfile(name="Family House", position=(4800.0, 5100.0, 0.0), footprint=(50, 50), floors=2)
    world.add_place(house_a)

    house_b = HouseProfile(name="Neighbour House 1", position=(4900.0, 5105.0, 0.0), footprint=(45, 45), floors=2)
    world.add_place(house_b)

    # People (profiles)
    world.people.append(PersonProfile(name="Alex", age=12, home_name="Family House", position_xyz=(4805.0, 5110.0, 0.0)))
    world.people.append(PersonProfile(name="Maya", age=11, home_name="Neighbour House 1", position_xyz=(4905.0, 5110.0, 0.0)))
    world.people.append(PersonProfile(name="Sam", age=13, home_name="Neighbour House 1", position_xyz=(4910.0, 5108.0, 0.0)))

    # Animals (profiles)
    world.animals.append(AnimalProfile(name="Rex", species="dog", color="black", position_xyz=(4803.0, 5106.0, 0.0)))
    world.animals.append(AnimalProfile(name="Luna", species="cat", color="white", position_xyz=(4908.0, 5112.0, 0.0)))

    # Agents
    observer = ObserverBot(name="Observer-1")
    world.add_agent(observer)

    walker = WalkerBot(name="Walker-1", start_xyz=house_a.position, world=world, return_interval=15)
    world.add_agent(walker)

    # Scouts
    world.add_scout(ScoutBot(name="Scout-Sound", mode="sound", center_xyz=house_a.position, extent_m=30, resolution_m=2.0))
    world.add_scout(ScoutBot(name="Scout-Light", mode="light", center_xyz=house_a.position, extent_m=30, resolution_m=2.0))

    # Surveyor
    surveyor = SurveyorBot(name="Surveyor-1", center_xyz=house_a.position, extent_m=30.0, resolution_m=2.0, height_m=8.0)
    world.set_surveyor(surveyor)

    return world