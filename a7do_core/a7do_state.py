from .body_state import BodyState
from .familiarity import Familiarity
from .memory import MemoryStore

class A7DOState:
    """
    Internal cognitive substrate.
    Does not control sleep/wake — only reflects state.
    """

    def __init__(self):
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)
        self.memory = MemoryStore()

        self.birthed = False
        self.is_awake = False
        self.perceived_place = "womb"

        self.internal_log = []

    def mark_birthed(self):
        self.birthed = True
        self.is_awake = True
        self.perceived_place = "hospital"
        self.familiarity.unlock()
        self.internal_log.append("birth: awareness unlocked")

    def log(self, msg: str):
        self.internal_log.append(msg)