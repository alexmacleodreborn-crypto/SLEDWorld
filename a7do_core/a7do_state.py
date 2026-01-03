from .body_state import BodyState
from .perceived_world import PerceivedWorld
from .familiarity import Familiarity
from .internal_log import InternalLog


class A7DOState:
    """
    A7DO Core Cognitive State

    This represents the being itself.
    No language.
    No concepts.
    No symbols.
    Only sensation, familiarity, and internal continuity.
    """

    def __init__(self):
        # Life state
        self.birthed: bool = False
        self.day: int = 0
        self.awake: bool = False

        # Core subsystems
        self.body = BodyState()
        self.world = PerceivedWorld()
        self.familiarity = Familiarity()
        self.log = InternalLog()

    # ─────────────────────────────
    # Lifecycle
    # ─────────────────────────────

    def mark_birth(self):
        if self.birthed:
            return

        self.birthed = True
        self.awake = True
        self.day = 0

        self.log.add(
            "birth: high-intensity sensory onset"
        )

    def wake(self):
        self.awake = True
        self.log.add(f"day {self.day} wake anchor")

    def sleep(self):
        self.awake = False

        # Sleep = replay + reinforcement
        replayed = self.familiarity.replay()

        self.log.add("sleep: replay and consolidation")
        for r in replayed:
            self.log.add(f"replay → {r}")

        self.day += 1

    # ─────────────────────────────
    # Sensory intake
    # ─────────────────────────────

    def experience(self, *, place: str, intensity: float, channels: dict):
        """
        Receive raw experience.
        channels example:
        {
            "light": 0.8,
            "noise": 1.0,
            "pressure": 0.6,
            "touch": 0.7
        }
        """

        if not self.birthed:
            return

        # Body reacts first
        self.body.apply_intensity(intensity)
        self.body.apply_channels(channels)

        # World awareness (place only)
        self.world.observe(place)

        # Familiarity learns patterns (NOT facts)
        self.familiarity.observe(
            place=place,
            channels=channels,
            intensity=intensity
        )

        self.log.add(
            f"experienced pattern={self.familiarity.last_pattern} place={place}"
        )