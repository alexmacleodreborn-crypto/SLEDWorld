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
    - Wake is NOT valid pre-birth
    - Sleep exists both pre- and post-birth (physiological)
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
        Wake transition.

        IMPORTANT:
        - Wake is INVALID pre-birth
        - Pre-birth arousal exists, but not 'wake'
        """
        if not self.aware:
            # Pre-birth: ignore wake entirely
            return

        self.body.wake()
        self.internal_log.append("wake: arousal increased")

    def sleep(self):
        """
        Sleep transition.

        - Valid pre-birth and post-birth
        - Triggers consolidation
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