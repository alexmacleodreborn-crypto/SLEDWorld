# world_core/world_grid.py

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class WorldGrid:
    """
    Objective 3D spatial frame.
    Units are abstract meters.
    No agents. No cognition.
    """

    size_x: int = 10_000
    size_y: int = 10_000
    size_z: int = 1_000   # height

    # Registered world objects (places, later agents)
    objects: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # --------------------------------------------------
    # Bounds
    # --------------------------------------------------

    def in_bounds(self, x: float, y: float, z: float) -> bool:
        return (
            0 <= x <= self.size_x and
            0 <= y <= self.size_y and
            0 <= z <= self.size_z
        )

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(self, obj):
        """
        Register a world object into the spatial grid.
        Object must expose:
        - name
        - position: (x, y, z)
        """
        x, y, z = obj.position

        if not self.in_bounds(x, y, z):
            raise ValueError(
                f"Object '{obj.name}' out of world bounds at {obj.position}"
            )

        self.objects[obj.name] = {
            "object": obj,
            "position": obj.position,
        }

    # --------------------------------------------------
    # Queries
    # --------------------------------------------------

    def get(self, name: str):
        return self.objects.get(name)

    def all(self):
        return list(self.objects.values())

    # --------------------------------------------------
    # Observer snapshot
    # --------------------------------------------------

    def snapshot(self):
        return {
            "size": {
                "x": self.size_x,
                "y": self.size_y,
                "z": self.size_z,
            },
            "volume": self.size_x * self.size_y * self.size_z,
            "objects": {
                name: data["position"]
                for name, data in self.objects.items()
            },
        }