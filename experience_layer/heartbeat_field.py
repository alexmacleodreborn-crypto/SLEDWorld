class HeartbeatField:
    """
    Continuous oscillatory biological signal.
    """

    def __init__(self, bpm: float, amplitude: float = 1.0, source: str = "unknown"):
        self.bpm = bpm
        self.amplitude = amplitude
        self.source = source

        self.phase = 0.0
        self.current_value = 0.0

    def tick(self, dt_seconds: float):
        # Convert BPM to Hz
        hz = self.bpm / 60.0
        self.phase += hz * dt_seconds

        # Simple pulse (can evolve later)
        self.current_value = self.amplitude * abs((self.phase % 1.0) - 0.5) * 2

    def snapshot(self):
        return {
            "bpm": self.bpm,
            "value": round(self.current_value, 3),
            "source": self.source,
        }