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
        footprint: tuple[float, float],   # (width, depth) in meters
        residents: int = 3,
        floors: int = 2,
    ):
        # Pass position tuple directly to WorldObject
        super().__init__(name=name, position=position)

        # Physical properties
        self.footprint = footprint
        self.residents = residents
        self.floors = floors

        # Derived physical size (simple, world-only)
        self.area = footprint[0] * footprint[1]

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "house",
            "footprint": {
                "width": self.footprint[0],
                "depth": self.footprint[1],
            },
            "area": self.area,
            "residents": self.residents,
            "floors": self.floors,
        })
        return base