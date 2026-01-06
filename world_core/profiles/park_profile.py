# world_core/profiles/park_profile.py

from world_core.world_object import WorldObject


class ParkProfile(WorldObject):
    """
    A public park in the world.

    - Pure world-layer object
    - Volumetric (XYZ)
    - Ground-based interaction space
    - Can contain sub-features later (pond, swings, chute)
    """

    # Interaction height (meters)
    PARK_HEIGHT = 3.0

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        size: tuple[float, float] = (200.0, 200.0),  # width, depth in meters
        trees: int = 20,
    ):
        super().__init__(name=name, position=position)

        self.size = (float(size[0]), float(size[1]))
        self.trees = int(trees)

        x, y, z = self.position

        # -----------------------------------------
        # World-space bounds (AUTHORITATIVE)
        # -----------------------------------------
        self.set_bounds(
            min_xyz=(x, y, z),
            max_xyz=(
                x + self.size[0],
                y + self.size[1],
                z + self.PARK_HEIGHT,
            ),
        )

        # -----------------------------------------
        # Sub-features (added later)
        # -----------------------------------------
        self.features: dict[str, WorldObject] = {}

    # =================================================
    # Observer snapshot
    # =================================================

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "park",
            "trees": self.trees,
            "size": list(self.size),
            "height": self.PARK_HEIGHT,
            "features": {
                name: feature.snapshot()
                for name, feature in self.features.items()
            },
        })
        return base