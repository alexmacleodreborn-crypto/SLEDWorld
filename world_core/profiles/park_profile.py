# world_core/profiles/park_profile.py

from world_core.world_object import WorldObject


class ParkProfile(WorldObject):
    """
    A public park in the world.
    Pure world-layer object.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        trees: int = 20,
        area: float = 200 * 200,  # m²
    ):
        x, y, z = position  # 🔧 unpack for WorldObject

        super().__init__(name, x, y, z)

        self.trees = trees
        self.area = area

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "park",
            "trees": self.trees,
            "area": self.area,
        })
        return base