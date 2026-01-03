# world_core/world_clock.py

class WorldClock:
    """
    Objective world time.
    Exists independently of A7DO awareness.

    Time model:
    - Day-based
    - Fractional hours
    - Condensed simulation (observer-controlled)
    """

    def __init__(self):
        self.day = 0
        self.hour = 0.0
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def tick(self, hours: float = 0.25):
        """
        Advance world time.
        Default: 15 minutes per tick.
        """
        if not self.running:
            return

        self.hour += hours

        if self.hour >= 24.0:
            self.hour -= 24.0
            self.day += 1

    @property
    def is_night(self) -> bool:
        return self.hour < 6.0 or self.hour >= 20.0

    def snapshot(self) -> dict:
        return {
            "day": self.day,
            "hour": round(self.hour, 2),
            "is_night": self.is_night,
        }