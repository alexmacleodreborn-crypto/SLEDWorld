import time


class WorldClock:
    """
    Continuous world clock.
    Runs even when A7DO is asleep or unborn.
    """

    def __init__(self):
        self.running = False
        self.last_tick = None
        self.time_minutes = 0.0

    def start(self):
        self.running = True
        self.last_tick = time.time()

    def tick(self, scale: float = 1.0):
        """
        Advances clock.
        scale = minutes per real second
        """
        if not self.running:
            return

        now = time.time()
        delta = now - self.last_tick
        self.last_tick = now

        self.time_minutes += delta * scale

    def snapshot(self):
        return {
            "world_time_minutes": round(self.time_minutes, 2),
            "running": self.running,
        }