# world_core/profiles/neighbourhood_profile.py

from __future__ import annotations
from world_core.world_object import WorldObject

class NeighbourhoodProfile(WorldObject):
    def __init__(self, name, position, size_xy=(240.0, 240.0), wrap=True):
        super().__init__(name=name, position=position)
        self.size_xy = size_xy
        self.wrap = wrap

        x, y, z = position
        w, h = size_xy
        self.set_bounds((x - w/2, y - h/2, z), (x + w/2, y + h/2, z + 20.0))

    def center_xyz(self):
        return self.position

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "neighbourhood",
            "size_xy": self.size_xy,
            "wrap": self.wrap,
        })
        return base