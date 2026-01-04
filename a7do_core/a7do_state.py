from .body_state import BodyState
from .familiarity import Familiarity
from .memory import MemoryStore


class A7DOState:
    """
    Subjective cognitive entity (A7DO).

    - No access to world time
    - No symbols
    - Phase changes only via gates
    """

    def __init__(self):
        # Core identity
        self.phase = "prebirth"   # prebirth | postbirth | infant | child
        self.aware = False

        # Internal systems
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)
        self.memory = MemoryStore()

        # Observer-visible internal log
        self.internal_log = []

    # ===============================
    # GATED TRANSITIONS
    # ===============================

    def unlock_awareness(self):
        if not self.aware:
            self.aware = True
            self.phase = "postbirth"
            self.familiarity.unlock()
            self.internal_log.append("birth: awareness unlocked")

    # ===============================
    # WAKE / SLEEP
    # ===============================

    def wake(self):
        if not self.aware:
            return
        self.body.wake()
        self.internal_log.append("wake")

    def sleep(self):
        self.body.sleep()
        replayed = self.familiarity.replay()
        self.internal_log.append(
            f"sleep: replayed {len(replayed)} patterns"
        )

    # ===============================
    # SNAPSHOT (observer only)
    # ===============================

    def snapshot(self):
        return {
            "phase": self.phase,
            "aware": self.aware,
            "body_awake": self.body.awake,
        }