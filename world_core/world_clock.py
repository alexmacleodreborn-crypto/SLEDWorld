# world_core/world_clock.py

from datetime import datetime, timedelta


class WorldClock:
    """
    Authoritative world time.

    - Tracks absolute world datetime
    - Can advance by world minutes OR real seconds
    - Independent of any agent cognition
    """

    def __init__(self, start_datetime=None, acceleration=60):
        # World datetime
        self.world_datetime = start_datetime or datetime(2025, 1, 1, 0, 0, 0)

        # How many WORLD seconds pass per REAL second
        self.acceleration = acceleration

    # =================================================
    # TIME ADVANCEMENT
    # =================================================

    def tick(self, *, minutes: float = None, real_seconds: float = None):
        """
        Advance world time.

        Provide ONE of:
        - minutes: advance by world minutes
        - real_seconds: advance by real seconds scaled by acceleration
        """

        if minutes is not None:
            delta = timedelta(minutes=float(minutes))

        elif real_seconds is not None:
            world_seconds = float(real_seconds) * float(self.acceleration)
            delta = timedelta(seconds=world_seconds)

        else:
            # Default: no-op
            return

        self.world_datetime += delta

    # =================================================
    # OBSERVER SNAPSHOT
    # =================================================

    def snapshot(self):
        return {
            "world_datetime": self.world_datetime.isoformat(sep=" "),
            "year": self.world_datetime.year,
            "month": self.world_datetime.month,
            "day": self.world_datetime.day,
            "hour": self.world_datetime.hour,
            "minute": self.world_datetime.minute,
            "second": self.world_datetime.second,
            "acceleration": self.acceleration,
        }