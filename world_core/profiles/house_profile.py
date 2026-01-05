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
        # ✅ PASS POSITION AS A SINGLE TUPLE (same as ParkProfile)
        super().__init__(name=name, position=position)

        # Physical properties
        self.footprint = footprint
        self.residents = residents
        self.floors = floors

        # Derived physical size
        self.area = float(footprint[0]) * float(footprint[1])

        # Optional: room layout (semantic, observer-only)
        self.rooms = {
            0: "living_room",
            1: "kitchen",
            2: "bathroom",
            3: "bedroom_1",
            4: "bedroom_2",
            5: "bedroom_3",
        }

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "house",
            "footprint": [float(self.footprint[0]), float(self.footprint[1])],
            "area": self.area,
            "residents": int(self.residents),
            "floors": int(self.floors),
            "rooms": self.rooms,
        })
        return base