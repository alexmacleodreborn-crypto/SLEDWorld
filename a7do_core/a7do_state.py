from .body_state import BodyState
from .familiarity import Familiarity
from .memory import MemoryStore


class A7DOState:
    """
    Subjective cognitive entity.
    Has NO access to world time.
    Phase is emergent, not scheduled.
    """

    def __init__(self):
        # -------------------------
        # Core identity
        # -------------------------
        self.phase = "prebirth"   # prebirth | postbirth | infant | child
        self.aware = False

        # -------------------------
        # Internal systems
        # -------------------------
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)
        self.memory = MemoryStore()

        # -------------------------
        # Internal log (observer-visible only)
        # -------------------------
        self.internal_log = []

    # --------------------------------------------------
    # Phase transitions (ONLY via gates)
    # --------------------------------------------------

    def unlock_awareness(self):
        if not self.aware:
            self.aware = True
            self.phase = "postbirth"
            self.familiarity.unlock()
            self.internal_log.append("birth: awareness unlocked")

    def snapshot(self):
        """
        Observer-only view of subjective state.
        """
        return {
            "phase": self.phase,
            "aware": self.aware,
        }