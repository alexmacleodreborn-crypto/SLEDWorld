import time


class WorldClock:
    def __init__(self):
        self.started = False
        self.last_time = None
        self.seconds_elapsed = 0.0

    def start(self):
        now = time.time()
        self.started = True
        self.last_time = now

    def tick(self):
        """
        Safe, self-healing tick.
        Works even if start() was never called.
        """
        now = time.time()

        if not self.started:
            self.started = True
            self.last_time = now
            return

        if self.last_time is None:
            self.last_time = now
            return

        delta = now - self.last_time
        self.last_time = now
        self.seconds_elapsed += delta

    @property
    def days_elapsed(self):
        # 1 simulated day = 24 real hours
        return self.seconds_elapsed / 86400.0

    def snapshot(self):
        return {
            "seconds_elapsed": round(self.seconds_elapsed, 2),
            "days_elapsed": round(self.days_elapsed, 4),
        }