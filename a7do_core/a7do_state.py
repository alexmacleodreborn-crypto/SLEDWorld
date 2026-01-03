from .body_state import BodyState
from .familiarity import Familiarity
from .memory import MemoryStore


class A7DOState:
    """
    Core internal state of A7DO.
    No world knowledge lives here.
    No symbols.
    No language.
    """

    def __init__(self):
        # Existence & awareness
        self.birthed = False
        self.is_awake = True

        # Subsystems
        self.body = BodyState()
        self.familiarity = Familiarity(gated=True)
        self.memory = MemoryStore()

        # Observer-visible phenomenology (NOT cognition)
        self.internal_log: list[str] = []

    # -------------------------
    # Lifecycle
    # -------------------------

    def mark_birth(self):
        """
        Birth opens the sensory gate.
        Prebirth patterns remain, but future imprinting is full strength.
        """
        self.birthed = True
        self.familiarity.unlock()
        self.internal_log.append("birth: sensory gate opened")

    def sleep(self):
        """
        Sleep closes awareness and triggers replay.
        """
        self.is_awake = False
        self.internal_log.append("sleep: replay and consolidation")

        replayed = self.familiarity.replay()
        if replayed:
            self.internal_log.append(
                f"replayed patterns: {replayed}"
            )

    def wake(self):
        """
        Awareness resumes.
        """
        self.is_awake = True
        self.internal_log.append("wake: awareness resumes")

    # -------------------------
    # Logging (observer only)
    # -------------------------

    def log(self, message: str):
        self.internal_log.append(message)