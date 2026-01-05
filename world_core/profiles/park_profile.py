# world_core/profiles/park_profile.py

from world_core.world_object import WorldObject

    
    class ParkProfile(WorldObject):
    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        trees: int = 10,
    ):
        super().__init__(name=name, position=position)
        self.trees = trees

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