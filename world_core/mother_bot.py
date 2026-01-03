class MotherBot:
    """
    Mother as a physiological field.
    No cognition, no memory.
    """

    def __init__(self):
        self.heartbeat_phase = 0.0
        self.heartbeat_rate = 1.0
        self.stress = 0.2
        self.activity = 0.3

    def tick(self, dt: float):
        self.heartbeat_phase = (
            self.heartbeat_phase + dt * self.heartbeat_rate
        ) % 1.0

        # slow stress drift
        self.stress = max(0.0, min(1.0, self.stress + dt * 0.002))

    def snapshot(self):
        return {
            "heartbeat_phase": round(self.heartbeat_phase, 3),
            "stress": round(self.stress, 3),
            "activity": round(self.activity, 3),
        }