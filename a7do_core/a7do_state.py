from .body_state import BodyState
from .familiarity import FamiliarityTracker
from .memory import MemoryStore


class A7DOState:
    def __init__(self):
        self.birthed = False
        self.is_awake = True

        self.body = BodyState()
        self.familiarity = FamiliarityTracker()
        self.memory = MemoryStore()

        # Observer-visible phenomenology
        self.internal_log: list[str] = []

    def mark_birth(self):
        self.birthed = True
        self.internal_log.append("birth: sensory onset")

    def log(self, message: str):
        self.internal_log.append(message)

    def sleep(self):
        self.is_awake = False
        self.internal_log.append("sleep: replay and consolidation")

    def wake(self):
        self.is_awake = True
        self.internal_log.append("wake: awareness resumes")