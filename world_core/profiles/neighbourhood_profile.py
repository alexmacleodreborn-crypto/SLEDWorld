# world_core/profiles/neighbourhood_profile.py

from world_core.world_object import WorldObject

class NeighbourhoodProfile(WorldObject):
    def __init__(self, name: str, position, size_m: float = 1200.0):
        super().__init__(name=name, position=position)
        x,y,z = position
        r = float(size_m)/2.0
        self.set_bounds(min_xyz=(x-r, y-r, z), max_xyz=(x+r, y+r, z+50.0))
        self.size_m = float(size_m)
        self.type = "neighbourhood"

    def snapshot(self):
        base = super().snapshot()
        base.update({"type":"neighbourhood","size_m": self.size_m})
        return base