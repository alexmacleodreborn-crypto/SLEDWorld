from world_core.world_object import WorldObject
from world_core.world_feature import WorldFeature


class HouseProfile(WorldObject):
    """
    Residential house with floors and rooms.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        footprint: tuple[float, float],
        floors: int = 2,
        residents: int = 3,
    ):
        x, y, z = position
        super().__init__(name, x, y, z)

        self.footprint = footprint
        self.floors = floors
        self.residents = residents
        self.area = footprint[0] * footprint[1]

        # -------------------------
        # Internal house layout
        # -------------------------
        self.rooms = {
            # Floor 0
            "living_room": WorldFeature(
                name="Living Room",
                kind="room",
                local_position=(10.0, 10.0, 0.0),
            ),
            "kitchen": WorldFeature(
                name="Kitchen",
                kind="room",
                local_position=(30.0, 10.0, 0.0),
            ),
            "toilet": WorldFeature(
                name="Toilet",
                kind="room",
                local_position=(45.0, 10.0, 0.0),
            ),

            # Floor 1 (z = height)
            "bedroom_1": WorldFeature(
                name="Bedroom 1",
                kind="room",
                local_position=(10.0, 10.0, 3.0),
            ),
            "bedroom_2": WorldFeature(
                name="Bedroom 2",
                kind="room",
                local_position=(30.0, 10.0, 3.0),
            ),
            "bathroom": WorldFeature(
                name="Bathroom",
                kind="room",
                local_position=(45.0, 10.0, 3.0),
            ),
        }

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "house",
            "floors": self.floors,
            "area": self.area,
            "residents": self.residents,
            "rooms": {
                name: room.snapshot()
                for name, room in self.rooms.items()
            },
        })
        return base