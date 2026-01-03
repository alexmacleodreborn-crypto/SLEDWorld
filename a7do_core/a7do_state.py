from .perceived_world import PerceivedWorld
from .body_state import BodyState
from .familiarity import FamiliarityStore
from .internal_log import InternalLog

class A7DOState:
    def __init__(self):
        self.birthed = False
        self.day_index = 0

        self.perceived = PerceivedWorld()
        self.body = BodyState()
        self.familiarity = FamiliarityStore()
        self.log = InternalLog()

    def mark_birthed(self):
        self.birthed = True
        self.log.add("birth: high-intensity sensory onset")

    def next_day(self):
        self.day_index += 1
        self.log.add(f"day {self.day_index} begins")