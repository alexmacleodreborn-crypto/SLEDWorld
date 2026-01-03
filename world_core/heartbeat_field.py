import math
import random

class HeartbeatField:
    """
    Physical rhythmic oscillator.
    Represents a biological heartbeat.
    This is NOT symbolic time.
    """

    def __init__(self, bpm_mean: float, bpm_variance: float, seed: int = 1):
        self.bpm_mean = bpm_mean
        self.bpm_variance = bpm_variance
        self.rng = random.Random(seed)
        self.phase = 0.0

    def tick(self, minutes: float) -> float:
        """
        Advance the heartbeat oscillator.

        Returns a normalized intensity 0.0–1.0
        """
        bpm = self.bpm_mean + self.rng.uniform(-self.bpm_variance, self.bpm_variance)
        hz = bpm / 60.0  # beats per second

        # advance phase (no notion of clock, only oscillation)
        self.phase += 2 * math.pi * hz * (minutes / 60.0)

        # normalize
        return (math.sin(self.phase) + 1.0) / 2.0