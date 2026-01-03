from dataclasses import dataclass

@dataclass
class WorldClock:
    day: int = 0
    hour: int = 0
    minute: int = 0
    running: bool = False

    def start(self):
        self.running = True

    def tick(self, minutes: int = 1):
        """Advance world time by N minutes."""
        if not self.running:
            return

        self.minute += minutes

        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1

        while self.hour >= 24:
            self.hour -= 24
            self.day += 1

    @property
    def days_elapsed(self):
        return self.day

    def snapshot(self):
        return {
            "day": self.day,
            "hour": self.hour,
            "minute": self.minute,
        }