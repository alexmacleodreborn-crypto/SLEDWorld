# world_core/world_clock.py

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class WorldClock:
    acceleration: float = 1.0
    world_datetime: datetime = field(default_factory=lambda: datetime.utcnow())
    frame_counter: int = 0

    def tick(self, minutes: int = 1, real_seconds: float = 0.0) -> None:
        if real_seconds > 0:
            delta = timedelta(seconds=real_seconds * self.acceleration)
        else:
            delta = timedelta(minutes=minutes)
        self.world_datetime = self.world_datetime + delta
        self.frame_counter += 1

    def snapshot(self):
        return {
            "world_datetime": self.world_datetime.isoformat(timespec="seconds"),
            "frame_counter": self.frame_counter,
            "acceleration": self.acceleration,
        }