# world_core/profiles/street_profile.py

from world_core.world_object import WorldObject

class StreetProfile(WorldObject):
    def __init__(self, name: str, position, length_m: float = 400.0, width_m: float = 16.0):
        super().__init__(name=name, position=position)
        x,y,z = position
        L = float(length_m)
        W = float(width_m)
        self.set_bounds(min_xyz=(x, y, z), max_xyz=(x+L, y+W, z+1.0))
        self.length_m = L
        self.width_m = W
        self.type = "street"

    def snapshot(self):
        base = super().snapshot()
        base.update({"type":"street","length_m": self.length_m, "width_m": self.width_m})
        return base