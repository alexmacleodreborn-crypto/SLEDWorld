from datetime import datetime, timedelta

class WorldClock:
    """
    Absolute world time.
    Owns time. Everyone else receives deltas.
    """

    def __init__(self, acceleration: float = 60.0):
        self.acceleration = acceleration  # world seconds per real second
        self.world_datetime = datetime(2025, 1, 1, 0, 0, 0)
        self.delta_minutes = 0.0

    def tick(self, seconds: float = 1.0):
        """
        Advance world time by `seconds * acceleration`.
        """
        delta = timedelta(seconds=seconds * self.acceleration)
        self.world_datetime += delta
        self.delta_minutes = delta.total_seconds() / 60.0

    def snapshot(self):
        return {
            "world_time": self.world_datetime.isoformat(),
            "delta_minutes": round(self.delta_minutes, 4),
            "acceleration": self.acceleration,
        }