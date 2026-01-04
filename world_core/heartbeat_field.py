import math


class HeartbeatField:
    """
    Simple oscillatory heartbeat signal.
    World-time driven.
    """

    def __init__(self, bpm: float = 80.0, amplitude: float = 1.0):
        self.bpm = bpm
        self.amplitude = amplitude
        self.phase = 0.0

    @property
    def hz(self) -> float:
        return self.bpm / 60.0

    def tick(self, minutes: float = 1.0):
        """
        Advance heartbeat by world-time minutes.
        """
        self.phase += 2 * math.pi * self.hz * (minutes / 60.0)

    def current_signal(self) -> float:
        """
        Instantaneous heartbeat signal (-amp → +amp)
        """
        return self.amplitude * math.sin(self.phase)

    def snapshot(self):
        return {
            "bpm": self.bpm,
            "amplitude": self.amplitude,
            "signal": round(self.current_signal(), 4),
        }