from .body_state import BodyState
from .familiarity import Familiarity
from .memory import MemoryStore


class A7DOState:
    """
    Subjective cognitive entity (A7DO).

    Core principles:
    - Has NO access to world time
    - No symbolic knowledge
    - Phase changes occur only through gated events
    - Wake / sleep are body-driven, not scheduled
    """

    def __init__(self):
        # --------------------------------------------------
        # Core identity
        # --------------------------------------------------
        self.phase = "prebirth"   # prebirth | postbirth | infant | child
        self.aware = False        # awareness gate (birth)

        # --------------------------------------------------
        # Internal systems (always present)
        # --------------------------------------------------
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)
        self.memory = MemoryStore()

        # --------------------------------------------------
        # Observer-visible internal log
        # --------------------------------------------------
        self.internal_log = []

    # ==================================================
    # GATED TRANSITIONS
    # ==================================================

    def unlock_awareness(self):
        """
        Birth gate.
        This is the ONLY place awareness becomes true.
        """
        if not self.aware:
            self.aware = True
            self.phase = "postbirth"
            self.familiarity.unlock()
            self.internal_log.append("birth: awareness unlocked")

    # ==================================================
    # WAKE / SLEEP (body-driven)
    # ==================================================

    def wake(self):
        """
        Transition to awake state.
        No concept of time — only internal arousal change.
        """
        self.body.wake()
        self.internal_log.append("wake: arousal increased")

    def sleep(self):
        """
        Transition to sleep state.
        Triggers internal consolidation.
        """
        self.body.sleep()

        # Sleep replay (pre-symbolic)
        replayed = self.familiarity.replay()
        if replayed:
            self.internal_log.append(
                f"sleep: replayed {len(replayed)} patterns"
            )
        else:
            self.internal_log.append("sleep: quiet consolidation")

    # ==================================================
    # OBSERVER SNAPSHOT
    # ==================================================

    def snapshot(self):
        """
        Observer-only view of subjective state.
        """
        return {
            "phase": self.phase,
            "aware": self.aware,
            "body_awake": self.body.awake,
        }