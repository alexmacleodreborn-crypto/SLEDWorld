from .body_state import BodyState
from .familiarity import Familiarity

class A7DOState:
    """
    The developing entity.
    """

    def __init__(self):
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)

        self.birthed = False
        self.aware = False

        self.internal_log = []

    def mark_birthed(self):
        self.birthed = True
        self.internal_log.append("birth: sensory shock")

    def unlock_awareness(self):
        self.aware = True
        self.familiarity.unlock()
        self.internal_log.append("awareness unlocked")