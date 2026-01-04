from .body_state import BodyState
from .familiarity import Familiarity
from .memory import MemoryStore


class A7DOState:
    """
    Subjective cognitive entity (A7DO).

    Core principles:
    - NO access to world time
    - NO symbolic reasoning
    - Phase transitions are gated
    - Wake / sleep are body-driven
    - Memory consolidation only post-birth
    """

    def __init__(self):
        # ==================================================
        # CORE IDENTITY
        # ==================================================
        self.phase = "prebirth"     # prebirth | postbirth | infant | child
        self.aware = False          # awareness gate (birth)

        # ==================================================
        # INTERNAL SYSTEMS (always exist)
        # ==================================================
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)
        self.memory = MemoryStore()

        # ==================================================
        # OBSERVER-ONLY LOG
        # ==================================================
        self.internal_log = []

    # ==================================================
    # GATED TRANSITIONS
    # ==================================================

    def unlock_awareness(self):
        """
        Birth gate.
        This is the ONLY place awareness becomes true.
        """
        if self.aware:
            return

        self.aware = True
        self.phase = "postbirth"
        self.familiarity.unlock()

        self.internal_log.append(
            "birth: awareness unlocked"
        )

    # ==================================================
    # WAKE / SLEEP (BODY-DRIVEN)
    # ==================================================

    def wake(self):
        """
        Transition to awake state.
        Prebirth wake has no meaning.
        """
        if not self.aware:
            # Prebirth: ignore wake attempts
            self.internal_log.append(
                "wake: prebirth (no awareness)"
            )
            return

        self.body.wake()
        self.internal_log.append(
            "wake: arousal increased"
        )

    def sleep(self):
        """
        Transition to sleep state.

        Prebirth:
        - physiological rest only
        - NO memory consolidation

        Postbirth:
        - familiarity replay
        - consolidation allowed
        """
        self.body.sleep()

        if not self.aware:
            # Prebirth sleep: no cognition
            self.internal_log.append(
                "sleep: prebirth physiological rest"
            )
            return

        # Postbirth consolidation
        replayed = self.familiarity.replay()

        if replayed:
            self.internal_log.append(
                f"sleep: replayed {len(replayed)} patterns"
            )
        else:
            self.internal_log.append(
                "sleep: quiet consolidation"
            )

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