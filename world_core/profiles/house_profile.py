# world_core/profiles/house_profile.py

from world_core.world_object import WorldObject


class HouseProfile(WorldObject):
    """
    A residential house in the world.
    Pure world-layer object.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        residents: int = 3,
        floors: int = 2,
    ):
        x, y, z = position  # 🔧 unpack tuple for WorldObject

        super().__init__(name, x, y, z)

        self.residents = residents
        self.floors = floors

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "house",
            "residents": self.residents,
            "floors": self.floors,
        })
        return base