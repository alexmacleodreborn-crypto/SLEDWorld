from world_core.world_object import WorldObject


class RoadProfile(WorldObject):
    """
    A road segment connecting places.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        length: int = 300,
        width: int = 12,
    ):
        super().__init__(name=name, position=position)

        self.length = length
        self.width = width

    def snapshot(self):
        return {
            "type": "road",
            "name": self.name,
            "position": self.position,
            "length": self.length,
            "width": self.width,
        }