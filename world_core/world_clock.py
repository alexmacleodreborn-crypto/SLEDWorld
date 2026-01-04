from datetime import datetime, timedelta

class WorldClock:
    """
    Single authoritative world time.
    """

    def __init__(self, start=None, acceleration=60):
        self.acceleration = acceleration  # world seconds per real second
        self.world_datetime = start or datetime(2025, 1, 1, 6, 0, 0)

    def tick(self, real_seconds=1.0):
        delta = timedelta(seconds=real_seconds * self.acceleration)
        self.world_datetime += delta

    def snapshot(self):
        return {
            "datetime": self.world_datetime.isoformat(),
            "hour": self.world_datetime.hour,
            "day": self.world_datetime.strftime("%A"),
            "is_day": 6 <= self.world_datetime.hour < 20,
        }