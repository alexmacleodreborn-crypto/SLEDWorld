# world_core/profiles/park_profile.py

import random
from world_core.world_object import WorldObject
from world_core.material import WOOD, GRASS

class ParkProfile:
    name = "park"

    def __init__(self, tree_count=20):
        self.tree_count = tree_count
        self.rng = random.Random(42)

    def generate(self, origin, size):
        ox, oy, oz = origin
        sx, sy, _ = size

        objects = []

        # Grass ground
        objects.append(
            WorldObject(
                "park_ground",
                "ground",
                (ox, oy, oz),
                (sx, sy, 1),
                GRASS,
            )
        )

        # Trees
        for i in range(self.tree_count):
            x = ox + self.rng.uniform(0, sx)
            y = oy + self.rng.uniform(0, sy)

            objects.append(
                WorldObject(
                    f"tree_{i}",
                    "tree",
                    (x, y, oz),
                    (1, 1, self.rng.uniform(6, 12)),
                    WOOD,
                )
            )

        return objects