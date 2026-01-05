from world_core.world_object import WorldObject
import random


class ParkProfile(WorldObject):
    """
    A park in the world.
    Exists independently of any observer.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        tree_count: int = 20,
        area_size: tuple[int, int] = (200, 200),
        seed: int = 1,
    ):
        super().__init__(name=name, position=position)

        self.tree_count = tree_count
        self.area_size = area_size
        self.rng = random.Random(seed)

        # Pre-generate trees (world truth)
        self.trees = [
            {
                "id": i,
                "offset": (
                    self.rng.uniform(-area_size[0] / 2, area_size[0] / 2),
                    self.rng.uniform(-area_size[1] / 2, area_size[1] / 2),
                    0,
                ),
            }
            for i in range(tree_count)
        ]

    def snapshot(self):
        return {
            "type": "park",
            "name": self.name,
            "position": self.position,
            "tree_count": self.tree_count,
            "area_size": self.area_size,
        }