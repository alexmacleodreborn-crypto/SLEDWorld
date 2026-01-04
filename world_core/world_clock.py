from datetime import datetime, timedelta


class WorldClock:
    """
    Accelerated real-world clock.
    """

    def __init__(self, acceleration: int = 60):
        self.acceleration = acceleration
        self.start_time = datetime(2025, 1, 1, 0, 0, 0)
        self.world_datetime = self.start_time
        self.total_minutes = 0.0

    def tick(self, minutes: float):
        """
        Advance world time deterministically.
        """
        self.total_minutes += minutes
        self.world_datetime = self.start_time + timedelta(minutes=self.total_minutes)

    def snapshot(self):
        return {
            "datetime": str(self.world_datetime),
            "total_minutes": round(self.total_minutes, 2),
            "day": int(self.total_minutes // (24 * 60)),
        }