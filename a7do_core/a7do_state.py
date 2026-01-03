# a7do_core/a7do_state.py

from .body_state import BodyState
from .familiarity import Familiarity
from .memory import MemoryStore

class A7DOState:
    """
    Internal cognitive state of A7DO.
    This is NOT the world. This is perception + body + familiarity.
    """

    def __init__(self):
        # Ontological state
        self.birthed = False
        self.is_awake = False

        # Perception mode (not location)
        # womb → hospital → home
        self.perception_mode = "womb"

        # Core subsystems
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)
        self.memory = MemoryStore()

        # Observer-visible log
        self.internal_log: list[str] = []

    # ---------- State transitions ----------

    def unlock_birth(self):
        """Internal awareness transition at birth."""
        self.birthed = True
        self.perception_mode = "hospital"
        self.familiarity.unlock()
        self.internal_log.append("birth: awareness unlocked")

    def wake(self):
        self.is_awake = True
        self.internal_log.append("wake")

    def sleep(self):
        self.is_awake = False
        replayed = self.familiarity.replay()
        self.internal_log.append("sleep: replay and consolidation")
        for p in replayed:
            self.internal_log.append(f"replay: {p}")

    def move_to(self, mode: str):
        """Observer-controlled perceptual transition."""
        self.perception_mode = mode
        self.internal_log.append(f"perception → {mode}")