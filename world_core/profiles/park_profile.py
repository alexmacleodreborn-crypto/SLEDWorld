from world_core.world_object import WorldObject


class ParkProfile(WorldObject):
    def __init__(self, name, position, trees=20):
        super().__init__(name=name, position=position)
        self.trees = int(trees)
        x, y, z = position
        self.set_bounds((x - 30, y - 30, z), (x + 30, y + 30, z + 1))

    def snapshot(self):
        base = super().snapshot()
        base.update({"type": "park", "trees": self.trees})
        return base