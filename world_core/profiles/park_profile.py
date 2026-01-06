# world_core/profiles/park_feature_profile.py

from world_core.world_object import WorldObject


class ParkFeatureProfile(WorldObject):
    """
    A physical feature inside a park (pond, swings, chute, etc).

    Rules:
    - Pure world-layer object
    - Has real XYZ volume
    - Used ONLY for geometric containment + semantic resolution
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
        x, y, z = self.position

        # -----------------------------------------
        # World-space bounds
        # -----------------------------------------
        self.min_xyz = (x, y, z)
        self.max_xyz = (
            x + float(width),
            y + float(depth),
            z + float(height),
        )

        # -----------------------------------------
        # Feature metadata
        # -----------------------------------------
        self.feature_type = feature_type
        self.size = {
            "width": float(width),
            "depth": float(depth),
            "height": float(height),
        }

    # -----------------------------------------
    # Geometry test (CRITICAL)
    # -----------------------------------------

    def contains_world_point(self, xyz: tuple[float, float, float]) -> bool:
        x, y, z = xyz
        return (
            self.min_xyz[0] <= x <= self.max_xyz[0]
            and self.min_xyz[1] <= y <= self.max_xyz[1]
            and self.min_xyz[2] <= z <= self.max_xyz[2]
        )

    # -----------------------------------------
    # Observer snapshot
    # -----------------------------------------

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