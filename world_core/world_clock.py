# world_core/world_clock.py

class WorldClock:
    """
    Canonical world time.
    Always running, independent of A7DO awareness.
    """

    def __init__(self):
        self.running = False
        self.minutes = 0.0  # world minutes since start

    def start(self):
        self.running = True

    def tick(self, delta_hours: float):
        if not self.running:
            return
        self.minutes += delta_hours * 60.0

    @property
    def days_elapsed(self) -> float:
        return self.minutes / (60.0 * 24.0)

    def snapshot(self):
        days = int(self.days_elapsed)
        hours = int((self.minutes % (60 * 24)) // 60)
        minutes = int(self.minutes % 60)

        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "total_minutes": round(self.minutes, 2),
        }