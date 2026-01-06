from world_core.world_object import WorldObject


class ParkFeatureProfile(WorldObject):
    """
    A physical feature inside a park (pond, swings, chute).
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        size: tuple[float, float, float],  # (width, depth, height)
        feature_type: str,
    ):
        super().__init__(name=name, position=position)

        width, depth, height = size
        x, y, z = position

        # World-space bounds
        self.min_xyz = (x, y, z)
        self.max_xyz = (
            x + width,
            y + depth,
            z + height,
        )

        self.size = {
            "width": float(width),
            "depth": float(depth),
            "height": float(height),
        }

        self.feature_type = feature_type

    # -----------------------------------------
    # Geometry test
    # -----------------------------------------

    def contains_world_point(self, xyz):
        x, y, z = xyz
        return (
            self.min_xyz[0] <= x <= self.max_xyz[0]
            and self.min_xyz[1] <= y <= self.max_xyz[1]
            and self.min_xyz[2] <= z <= self.max_xyz[2]
        )

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "park_feature",
            "feature_type": self.feature_type,
            "size": self.size,
            "bounds": {
                "min": self.min_xyz,
                "max": self.max_xyz,
            },
        })
        return base