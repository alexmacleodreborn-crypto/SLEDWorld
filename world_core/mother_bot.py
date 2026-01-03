import math

class MotherBot:
    """
    Represents the mother as a rhythmic, regulating field.
    No cognition. No intent. Just physiology + environment filter.
    """

    def __init__(self):
        self.heartbeat_phase = 0.0
        self.heartbeat_rate = 1.0  # slower than infant
        self.stress = 0.2          # baseline calm
        self.activity = 0.3        # movement / walking etc.

    def tick(self, dt: float):
        self.heartbeat_phase = (
            self.heartbeat_phase + dt * self.heartbeat_rate
        ) % 1.0

        # Stress drifts slowly
        self.stress += dt * 0.005
       