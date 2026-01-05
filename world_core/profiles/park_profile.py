from world_core.world_object import WorldObject
from world_core.world_feature import WorldFeature


class ParkProfile(WorldObject):
    """
    A public park in the world.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        trees: int = 20,
    ):
        x, y, z = position
        super().__init__(name, x, y, z)

        self.trees = trees
        self.area = 200 * 200  # m²

        # -------------------------
        # Internal park layout
        # -------------------------
        self.features = {
            "duck_pond": WorldFeature(
                name="Duck Pond",
                kind="pond",
                local_position=(30.0, 40.0, 0.0),
            ),
            "swing": WorldFeature(
                name="Swing",
                kind="play_equipment",
                local_position=(80.0, 20.0, 0.0),
            ),
            "chute": WorldFeature(
                name="Chute",
                kind="play_equipment",
                local_position=(60.0, 70.0, 0.0),
            ),
        }

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "park",
            "trees": self.trees,
            "area": self.area,
            "features": {
                name: feat.snapshot()
                for name, feat in self.features.items()
            },
        })
        return base