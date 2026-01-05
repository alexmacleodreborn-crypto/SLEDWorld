# world_core/profiles/park_profile.py

from world_core.world_object import WorldObject

class ParkProfile(WorldObject):
    """
    Physical park in world space.
    """

    def __init__(self, name="Central Park", x=5000, y=5000, z=0):
        super().__init__(name, x, y, z)

        self.trees = 20
        self.area = 200 * 200  # m²

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "park",
            "trees": self.trees,
            "area": self.area,
        })
        return base