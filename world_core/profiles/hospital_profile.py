from world_core.world_object import WorldObject


class HospitalProfile(WorldObject):
    """
    Medical facility.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        floors: int = 4,
        rooms: int = 40,
    ):
        super().__init__(name=name, position=position)

        self.floors = floors
        self.rooms = rooms

    def snapshot(self):
        return {
            "type": "hospital",
            "name": self.name,
            "position": self.position,
            "floors": self.floors,
            "rooms": self.rooms,
        }