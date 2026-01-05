from world_core.world_object import WorldObject


class HouseProfile(WorldObject):
    """
    A residential building.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        floors: int = 2,
        footprint: tuple[int, int] = (50, 50),
    ):
        super().__init__(name=name, position=position)

        self.floors = floors
        self.footprint = footprint

    def snapshot(self):
        return {
            "type": "house",
            "name": self.name,
            "position": self.position,
            "floors": self.floors,
            "footprint": self.footprint,
        }