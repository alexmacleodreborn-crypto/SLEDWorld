# world_core/world_grid.py

from dataclasses import dataclass

@dataclass
class WorldGrid:
    """
    Objective 3D spatial frame.
    Units are abstract meters.
    """

    size_x: int = 10_000
    size_y: int = 10_000
    size_z: int = 1_000   # height

    def in_bounds(self, x: float, y: float, z: float) -> bool:
        return (
            0 <= x <= self.size_x and
            0 <= y <= self.size_y and
            0 <= z <= self.size_z
        )

    def snapshot(self):
        return {
            "size": {
                "x": self.size_x,
                "y": self.size_y,
                "z": self.size_z,
            },
            "volume": self.size_x * self.size_y * self.size_z,
        }