import math

class HeartbeatField:
    """
    Continuous heartbeat signal driven by world time.
    """

    def __init__(self, bpm: float):
        self.bpm = bpm

    def sample(self, world_minutes: float) -> float:
        phase = (world_minutes * self.bpm) % 60
        return max(0.0, math.sin(phase / 60 * 2 * math.pi))