# world_core/profiles/park_profile.py

from world_core.world_object import WorldObject


class ParkProfile(WorldObject):
    """
    A public park in the world.
    Exists purely at the world layer.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        trees: int = 20,
        area: float = 200 * 200,  # m²
    ):
        super().__init__(name=name, position=position)

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