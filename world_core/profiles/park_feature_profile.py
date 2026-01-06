# world_core/profiles/park_feature_profile.py

import random
from world_core.world_object import WorldObject


class ParkFeatureProfile(WorldObject):
    """
    A physical feature inside a park (pond, swings, chute).

    Rules:
    - Pure world-layer object
    - Real 3D volume in WORLD coordinates
    - No agents
    - No cognition
    - No time
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

        # -----------------------------------------
        # World-space bounding box (AUTHORITATIVE)
        # -----------------------------------------
        self.set_bounds(
            min_xyz=(x, y, z),
            max_xyz=(x + width, y + depth, z + height),
        )

        # -----------------------------------------
        # Physical properties
        # -----------------------------------------
        self.size = {
            "width": float(width),
            "depth": float(depth),
            "height": float(height),
        }

        self.feature_type = str(feature_type)

        # Canonical semantic label
        self.label = f"park_feature:{self.feature_type}"

    # =================================================
    # Spatial helpers (for walkers)
    # =================================================

    def random_point_inside(self) -> tuple[float, float, float]:
        """
        Return a random WORLD-space point inside this feature.
        """
        (min_x, min_y, min_z), (max_x, max_y, max_z) = self.bounds

        return (
            random.uniform(min_x, max_x),
            random.uniform(min_y, max_y),
            random.uniform(min_z, max_z),
        )

    # -----------------------------------------
    # Observer snapshot
    # -----------------------------------------

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "park_feature",
            "label": self.label,
            "feature_type": self.feature_type,
            "size": self.size,
        })
        return base