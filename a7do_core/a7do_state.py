from .body_state import BodyState
from .perceived_world import PerceivedWorld
from .familiarity import Familiarity
from .internal_log import InternalLog

class A7DOState:
    """
    Proto-being exists prebirth.
    Birth is a transition unlock, not creation.
    """

    def __init__(self):
        self.exists = True
        self.birthed = False
        self.day = 0
        self.awake = False

        self.body = BodyState(prebirth=True)
        self.world = PerceivedWorld()
        self.familiarity = Familiarity(gated=True)
        self.log = InternalLog()

        self.log.add("proto-state: pre-birth continuity")

    def mark_birth(self):
        """
        Transition: world anchoring threshold.
        """
        if self.birthed:
            return
        self.birthed = True
        self.awake = True
        self.day = 0

        self.body.unlock_birth_transition()
        self.familiarity.unlock()

        self.log.add("birth: transition threshold crossed (gain unlocked)")

    def next_day(self):
        self.day += 1
        self.log.add(f"day {self.day} begins")