# world_core/profiles/park_profile.py

from __future__ import annotations
from world_core.world_object import WorldObject

class ParkProfile(WorldObject):
    def __init__(self, name, position, size_xy=(60.0, 60.0), trees=20):
        super().__init__(name=name, position=position)
        self.size_xy = size_xy
        self.trees = int(trees)

        x, y, z = position
        w, h = size_xy
        self.set_bounds((x - w/2, y - h/2, z), (x + w/2, y + h/2, z + 3.0))

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "park",
            "size_xy": self.size_xy,
            "trees": self.trees,
        })
        return base