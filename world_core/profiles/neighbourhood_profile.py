# world_core/profiles/neighbourhood_profile.py

from __future__ import annotations
from world_core.world_object import WorldObject


class NeighbourhoodProfile(WorldObject):
    """
    Top-level spatial container.

    - Represents a neighbourhood / district
    - Provides wraparound (globe / torus) boundary
    - No semantics, no cognition
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        size_m: float = 1000.0,
    ):
        super().__init__(name=name, position=position)

        self.size_m = float(size_m)

        half = self.size_m / 2.0
        x, y, z = position

        # World-space bounds (wraparound domain)
        self.set_bounds(
            min_xyz=(x - half, y - half, z),
            max_xyz=(x + half, y + half, z + 100.0),
        )

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "neighbourhood",
            "size_m": self.size_m,
        })
        return base