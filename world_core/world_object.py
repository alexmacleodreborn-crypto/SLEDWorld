class WorldObject:
    """
    Base class for any physical object or place in the world.
    """

    def __init__(self, name: str, position: tuple[float, float, float]):
        self.name = name
        self.position = position  # (x, y, z)

    def tick(self, real_seconds: float):
        """
        Optional world update.
        """
        pass

    def snapshot(self):
        return {
            "name": self.name,
            "position": self.position,
        }