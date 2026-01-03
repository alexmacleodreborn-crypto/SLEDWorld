from .physiology import Physiology
from .body_state import BodyState
from .familiarity import Familiarity

class A7DOState:
    def __init__(self):
        self.body = BodyState()
        self.phys = Physiology()
        self.familiarity = Familiarity(gated=True)

        self.internal_log = []

        self.is_awake = False
        self.birthed = False

    def tick(self, dt: float):
        self.phys.tick(dt)

        if self.phys.pressure >= 1.0:
            self.internal_log.append("pressure release")
            self.phys.pressure *= 0.5

        if self.is_awake and self.phys.fatigue >= 1.2:
            self.internal_log.append("fatigue → sleep")
            self.sleep()

    def wake(self):
        if not self.is_awake:
            self.is_awake = True
            self.body.wake()
            self.internal_log.append("wake")

    def sleep(self):
        if self.is_awake:
            self.is_awake = False
            self.body.sleep()
            replayed = self.familiarity.replay()
            self.internal_log.append(f"sleep replay {replayed}")

    def mark_birthed(self):
        if not self.birthed:
            self.birthed = True
            self.familiarity.unlock()
            self.internal_log.append("birth transition")