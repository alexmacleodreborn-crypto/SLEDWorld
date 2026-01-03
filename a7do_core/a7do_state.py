# a7do_core/a7do_state.py

from .body_state import BodyState
from .familiarity import Familiarity
from .memory import MemoryStore

class A7DOState:
    """
    Internal cognitive state of A7DO.
    """

    def __init__(self):
        # Ontological flags
        self.birthed = False
        self.is_awake = False

        # Perception mode (not location)
        self.perception_mode = "womb"  # locked pre-birth

        # Time counters
        self.gestation_cycles = 0  # pre-birth wake/sleep cycles

        # Core subsystems
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)
        self.memory = MemoryStore()

        # Observer-visible log
        self.internal_log: list[str] = []

    # ---------- Pre-birth physiology ----------

    def prebirth_wake(self):
        if self.birthed:
            return
        self.is_awake = True
        self.internal_log.append("prebirth: wake")

    def prebirth_sleep(self):
        if self.birthed:
            return
        self.is_awake = False
        self.gestation_cycles += 1

        replayed = self.familiarity.replay()
        self.internal_log.append("prebirth: sleep (muted)")
        for p in replayed:
            self.internal_log.append(f"prebirth replay: {p}")

    # ---------- Birth transition ----------

    def unlock_birth(self):
        """
        One-way awareness transition.
        """
        self.birthed = True
        self.is_awake = True

        self.perception_mode = "hospital"
        self.familiarity.unlock()

        self.internal_log.append("birth: awareness unlocked")