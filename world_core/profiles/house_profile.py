from world_core.world_object import WorldObject
from world_core.profiles.room_profile import RoomProfile


class HouseProfile(WorldObject):
    def __init__(self, name, position, footprint=(50, 50), floors=2):
        super().__init__(name=name, position=position)

        w, d = footprint
        x, y, z = position
        self.footprint = footprint
        self.floors = int(floors)

        self.set_bounds(min_xyz=(x, y, z), max_xyz=(x + w, y + d, z + floors * 3))

        self.rooms = {}
        self._build_rooms()

    def _build_rooms(self):
        x, y, z = self.position

        # living room on ground floor
        living = RoomProfile(
            name=f"{self.name}:LivingRoom",
            position=(x + 2, y + 2, z),
            size=(20, 20, 3),
            floor=0,
            room_type="living_room",
        )
        self.rooms[living.name] = living

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "house",
            "footprint": self.footprint,
            "floors": self.floors,
            "rooms": list(self.rooms.keys()),
        })
        return base