class WorldClock:
    def __init__(self, world):
        self.world = world

    def advance(self, hours: float):
        self.world.tick(hours)