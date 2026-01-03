from .body_state import BodyState
from .familiarity import Familiarity


class A7DOState:
    def __init__(self):
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)

        self.birthed = False
        self.is_awake = False
        self.internal_log = []

    def tick(self, dt_seconds: float):
        self.body.tick(dt_seconds)

    def mark_birthed(self):
        self.birthed = True
        self.familiarity.unlock()
        self.internal_log.append("birth: sensory shock")

    def wake(self):
        self.is_awake = True
        self.internal_log.append("wake")

    def sleep(self):
        self.is_awake = False
        replayed = self.familiarity.replay()
        self.internal_log.append(f"sleep: replay {replayed}")