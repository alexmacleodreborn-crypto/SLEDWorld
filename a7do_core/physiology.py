import random

class Physiology:
    def __init__(self):
        self.heartbeat_phase = 0.0
        self.pressure = 0.2
        self.arousal = 0.3
        self.fatigue = 0.0
        self.movement_noise = 0.0

        self._rng = random.Random(7)

    def tick(self, dt: float):
        # Heartbeat (cyclic)
        self.heartbeat_phase = (self.heartbeat_phase + dt * 1.2) % 1.0

        # Pressure drifts upward slowly
        self.pressure += dt * 0.02

        # Fatigue builds
        self.fatigue += dt * 0.015

        # Spontaneous micro-movement
        self.movement_noise = self._rng.uniform(0.0, 1.0)

    def snapshot(self):
        return {
            "heartbeat": round(self.heartbeat_phase, 2),
            "pressure": round(self.pressure, 2),
            "fatigue": round(self.fatigue, 2),
            "movement": round(self.movement_noise, 2),
        }