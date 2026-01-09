# world_core/profiles/road_profile.py

from __future__ import annotations
from world_core.world_object import WorldObject

class RoadProfile(WorldObject):
    def __init__(self, name, position, length=200, width=10, orientation="horizontal"):
        super().__init__(name=name, position=position)
        self.length = float(length)
        self.width = float(width)
        self.orientation = orientation

        x, y, z = position
        if orientation == "horizontal":
            self.set_bounds((x, y, z), (x + self.length, y + self.width, z + 1.0))
        else:
            self.set_bounds((x, y, z), (x + self.width, y + self.length, z + 1.0))

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "road",
            "length": self.length,
            "width": self.width,
            "orientation": self.orientation,
        })
        return base