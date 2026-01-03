# sledworld/world_core/heartbeat_field.py

import math
import random

class HeartbeatField:
    """
    Continuous heartbeat signal generator.
    Used by mother bot and A7DO internal body.
    """

    def __init__(self, bpm: float, noise: float = 0.05, seed: int = 1):
        self.bpm = bpm
        self.noise = noise
        self.phase = 0.0
        self.rng = random.Random(seed)

    def tick(self, dt_seconds: float) -> float:
        """
        Advance heartbeat by dt (seconds).
        Returns instantaneous intensity (0–1).
        """
        # Convert BPM to angular velocity
        omega = 2 * math.pi * (self.bpm / 60.0)
        self.phase += omega * dt_seconds

        base = 0.5 + 0.5 * math.sin(self.phase)
        jitter = self.rng.uniform(-self.noise, self.noise)

        return max(0.0, min(1.0, base + jitter))