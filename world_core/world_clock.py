class WorldClock:
    def __init__(self, acceleration=1):
        self.acceleration = acceleration
        self.total_minutes = 0

    def tick(self, minutes=1):
        self.total_minutes += int(minutes) * int(self.acceleration)

    def snapshot(self):
        return {"total_minutes": self.total_minutes, "acceleration": self.acceleration}