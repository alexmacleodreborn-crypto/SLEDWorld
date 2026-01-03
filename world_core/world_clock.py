# world_core/world_clock.py
import time

class WorldClock:
    def __init__(self, acceleration: float = 15.0):
        """
        acceleration = world minutes per real second
        e.g. 15 → 1 real second = 15 world minutes
        """
        self.acceleration = acceleration
        self.start_real = time.time()
        self.last_real = self.start_real

        self.world_minutes = 0.0

    def tick(self):
        now = time.time()
        delta_real = now - self.last_real
        self.last_real = now

        self.world_minutes += delta_real * self.acceleration

    @property
    def days_elapsed(self):
        return self.world_minutes / (60 * 24)

    def snapshot(self):
        return {
            "world_minutes": round(self.world_minutes, 2),
            "world_hours": round(self.world_minutes / 60, 2),
            "world_days": round(self.days_elapsed, 3),
            "acceleration": self.acceleration,
        }