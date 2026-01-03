from .body_state import BodyState
from .familiarity import Familiarity

class A7DOState:
    """
    Core organism state.
    No symbols, no language, no self-concept.
    """

    def __init__(self):
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)
        self.birthed = False
        self.is_awake = False
        self.internal_log = []

    def mark_birthed(self):
        self.birthed = True
        self.internal_log.append("birth: high-intensity sensory onset")

    def wake(self):
        self.is_awake = True
        self.internal_log.append("wake")

    def sleep(self):
        self.is_awake = False
        self.internal_log.append("sleep")

    # ---------- Observer visibility helpers ----------

    def body_snapshot(self):
        return self.body.snapshot()

    def familiarity_snapshot(self):
        return {
            "gated": self.familiarity.gated,
            "top_patterns": self.familiarity.top(5),
            "last_pattern": self.familiarity.last_pattern,
        }