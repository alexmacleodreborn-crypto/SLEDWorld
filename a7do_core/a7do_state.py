from a7do_core.body_state import BodyState
from a7do_core.familiarity import Familiarity
from a7do_core.memory import MemoryStore


class A7DOState:
    """
    Core internal state of A7DO.
    Represents the organism, not the world.
    """

    def __init__(self):
        # -------------------------
        # Lifecycle flags
        # -------------------------
        self.prebirth = True
        self.birthed = False
        self.is_awake = False

        # -------------------------
        # Internal systems
        # -------------------------
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)
        self.memory = MemoryStore()

        # -------------------------
        # Observer-visible log
        # -------------------------
        self.internal_log: list[str] = []

    # -------------------------
    # Lifecycle transitions
    # -------------------------

    def unlock_awareness(self):
        """
        Transition from pre-birth to aware organism.
        Called exactly once at birth.
        """
        if self.birthed:
            return

        self.prebirth = False
        self.birthed = True

        # Lift sensory gating
        self.familiarity.unlock()

        self.internal_log.append("awareness unlocked")

    # -------------------------
    # Convenience helpers
    # -------------------------

    def snapshot(self):
        return {
            "prebirth": self.prebirth,
            "birthed": self.birthed,
            "awake": self.is_awake,
        }