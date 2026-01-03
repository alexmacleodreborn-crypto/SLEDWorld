from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class WorldClock:
    """
    Objective world clock.
    Exists independently of A7DO.
    Accelerated relative to real time.
    """

    # Acceleration: how many WORLD seconds pass per REAL second
    acceleration: float = 1000.0

    # Internal state
    start_real: datetime = None
    last_real: datetime = None
    world_time: datetime = None

    def __post_init__(self):
        now = datetime.utcnow()
        self.start_real = now
        self.last_real = now

        # World starts at an absolute epoch
        self.world_time = datetime(
            year=2026,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
        )

    # --------------------------------------------------
    # Core tick
    # --------------------------------------------------

    def tick(self, real_seconds: float = None):
        """
        Advance world time.

        If real_seconds is None, uses wall-clock delta.
        Otherwise advances deterministically.
        """
        now = datetime.utcnow()

        if real_seconds is None:
            delta_real = (now - self.last_real).total_seconds()
        else:
            delta_real = float(real_seconds)

        if delta_real <= 0:
            return

        self.last_real = now

        # Accelerated advance
        delta_world = timedelta(
            seconds=delta_real * self.acceleration
        )
        self.world_time += delta_world

    # --------------------------------------------------
    # Read-only helpers (Observer only)
    # --------------------------------------------------

    @property
    def world_datetime(self) -> datetime:
        return self.world_time

    @property
    def world_day_index(self) -> int:
        """
        Day count since world epoch.
        """
        epoch = datetime(2026, 1, 1)
        return (self.world_time - epoch).days

    @property
    def world_time_of_day(self) -> str:
        return self.world_time.strftime("%H:%M:%S")

    def snapshot(self) -> dict:
        """
        Observer-visible snapshot.
        """
        return {
            "world_datetime": self.world_time.isoformat(),
            "world_day": self.world_day_index,
            "time_of_day": self.world_time_of_day,
            "acceleration": self.acceleration,
        }