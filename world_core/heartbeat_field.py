import math
import random

class HeartbeatField:
    """
    Continuous heartbeat oscillator.
    Exists entirely in world time.
    No cognition, no symbols.
    """

    def __init__(self, bpm: float = 80.0, variability: float = 5.0, seed: int | None = None):
        self.base_bpm = bpm
        self.variability = variability
        self.phase = 0.0

        self.rng = random.Random(seed)

    # -----------------------------------------
    # WORLD TIME ADVANCE
    # -----------------------------------------

    def tick_minutes(self, minutes: float):
        """
        Advance heartbeat oscillator by world minutes.
        """
        # Slight biological variability
        bpm = self.base_bpm + self.rng.uniform(-self.variability, self.variability)
        hz = bpm / 60.0

        # Advance phase
        self.phase += 2 * math.pi * hz * minutes

    # -----------------------------------------
    # CURRENT SIGNAL
    # -----------------------------------------

    def current(self) -> float:
        """
        Returns normalized heartbeat signal [0..1].
        """
        return 0.5 + 0.5 * math.sin(self.phase)