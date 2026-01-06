from world_core.world_object import WorldObject


class ParkProfile(WorldObject):
    """
    A public park in the world.

    - Has real world-space volume
    - Can later contain features (pond, swings, chute)
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        size: tuple[float, float] = (200.0, 200.0),  # width, depth
        trees: int = 20,
    ):
        super().__init__(name=name, position=position)

        self.size = (float(size[0]), float(size[1]))
        self.trees = int(trees)

        x, y, z = self.position

        # -----------------------------------------
        # World-space bounds (CRITICAL)
        # -----------------------------------------
        self.min_xyz = (x, y, z)
        self.max_xyz = (
            x + self.size[0],
            y + self.size[1],
            z + 5.0,  # shallow vertical extent
        )

        # Placeholder for future features
        self.features = {}

    # =================================================
    # Geometry
    # =================================================

    def contains_world_point(self, xyz):
        x, y, z = xyz
        return (
            self.min_xyz[0] <= x <= self.max_xyz[0]
            and self.min_xyz[1] <= y <= self.max_xyz[1]
            and self.min_xyz[2] <= z <= self.max_xyz[2]
        )

    # =================================================
    # Observer snapshot
    # =================================================

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "park",
            "trees": self.trees,
            "size": list(self.size),
            "bounds": {
                "min": self.min_xyz,
                "max": self.max_xyz,
            },
            "features": {
                name: feature.snapshot()
                for name, feature in self.features.items()
            },
        })
        return base