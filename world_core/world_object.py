# world_core/world_object.py

class WorldObject:
    """
    Any physical object in the world grid.
    """

    def __init__(self, name: str, x: float, y: float, z: float = 0.0):
        self.name = name
        self.position = {
            "x": float(x),
            "y": float(y),
            "z": float(z),
        }

    def move(self, dx=0.0, dy=0.0, dz=0.0):
        self.position["x"] += dx
        self.position["y"] += dy
        self.position["z"] += dz

    def snapshot(self):
        return {
            "name": self.name,
            "position": self.position,
        }