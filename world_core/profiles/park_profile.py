from world_core.world_object import WorldObject
from world_core.profiles.park_feature_profile import ParkFeatureProfile


class ParkProfile(WorldObject):
    """
    A public park in the world.
    Contains physical sub-areas (pond, swings, chute).
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
        # Park world bounds
        # -----------------------------------------
        self.min_xyz = (x, y, z)
        self.max_xyz = (
            x + self.size[0],
            y + self.size[1],
            z + 5.0,  # shallow vertical extent
        )

        # -----------------------------------------
        # Park features
        # -----------------------------------------
        self.features: dict[str, ParkFeatureProfile] = {}
        self._build_features()

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
    # Feature construction
    # =================================================

    def _build_features(self):
        base_x, base_y, base_z = self.position

        self.features["duck_pond"] = ParkFeatureProfile(
            name=f"{self.name}:duck_pond",
            position=(base_x + 30, base_y + 30, base_z),
            size=(40, 40, 2),
            feature_type="duck_pond",
        )

        self.features["swings"] = ParkFeatureProfile(
            name=f"{self.name}:swings",
            position=(base_x + 100, base_y + 40, base_z),
            size=(30, 20, 4),
            feature_type="swings",
        )

        self.features["chute"] = ParkFeatureProfile(
            name=f"{self.name}:chute",
            position=(base_x + 140, base_y + 120, base_z),
            size=(20, 30, 6),
            feature_type="chute",
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