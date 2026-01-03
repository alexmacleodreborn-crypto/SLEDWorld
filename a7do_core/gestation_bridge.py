from dataclasses import dataclass, field
from typing import Dict
from a7do_core.body_state import BodyState
from a7do_core.familiarity import Familiarity
from world_core.world_clock import WorldClock


@dataclass
class GestationBridge:
    """
    Handles pre-birth sensory exposure.
    A7DO is not awake, but patterns are recorded at reduced weight.
    """

    body: BodyState = field(default_factory=BodyState)
    familiarity: Familiarity = field(default_factory=lambda: Familiarity(gated=True))
    elapsed_days: float = 0.0

    def tick(self, clock: WorldClock):
        """
        Advance gestation exposure based on world time.
        """
        self.elapsed_days = clock.days_elapsed

        # Constant internal heartbeat (self)
        self.body.apply_intensity(0.2)

        # External maternal rhythm (filtered)
        self.familiarity.observe(
            place="womb",
            channels={
                "heartbeat": 0.9,
                "motion": 0.4,
                "muffled_sound": 0.3,
            },
            intensity=0.3,
        )

    def ready_for_birth(self) -> bool:
        """
        Threshold for transition to birth.
        """
        return self.elapsed_days >= 180  # ~6 months symbolic threshold