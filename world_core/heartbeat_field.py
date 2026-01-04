import math

class HeartbeatField:
    """
    Simple phase-based heartbeat oscillator.
    Phase advances based on elapsed minutes.
    """

    def __init__(self, bpm: float = 80.0):
        self.bpm = bpm
        self.phase = 0.0

    def tick(self, minutes: float):
        """
        Advance heartbeat phase.

        minutes: elapsed time in minutes (float)
        """
        if minutes <= 0:
            return self.phase

        hz = self.bpm / 60.0  # beats per second
        self.phase += 2 * math.pi * hz * (minutes / 60.0)
        self.phase %= 2 * math.pi
        return self.phase