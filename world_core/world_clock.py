import time

class WorldClock:
    """
    Continuous real-time-driven world clock.
    """

    def __init__(self, acceleration_minutes_per_second: float = 15.0):
        self.acceleration = acceleration_minutes_per_second
        self.last_real = time.time()
        self.world_minutes = 0.0

    def tick(self):
        now = time.time()
        delta = now - self.last_real
        self.last_real = now
        self.world_minutes += delta * self.acceleration

    @property
    def days_elapsed(self) -> float:
        return self.world_minutes / (60 * 24)

    def snapshot(self):
        return {
            "world_minutes": round(self.world_minutes, 2),
            "world_hours": round(self.world_minutes / 60, 2),
            "world_days": round(self.days_elapsed, 3),
            "acceleration": self.acceleration,
        }