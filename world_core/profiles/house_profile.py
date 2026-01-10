from world_core.world_object import WorldObject
from world_core.profiles.room_profile import RoomProfile

class HouseProfile(WorldObject):
    def __init__(self, name, position, footprint=(50, 50), floors=2):
        super().__init__(name=name, position=position)
        w, d = footprint
        x, y, z = position
        self.floors = int(floors)
        self.footprint = (float(w), float(d))
        self.set_bounds(min_xyz=(x, y, z), max_xyz=(x+w, y+d, z+3.0*floors))

        self.rooms = {}
        self._build_rooms()

    def _build_rooms(self):
        (min_x, min_y, min_z), (max_x, max_y, max_z) = self.bounds
        w = (max_x - min_x)
        d = (max_y - min_y)

        # One living room at ground
        living = RoomProfile(
            name=f"{self.name}:Living Room",
            position=(min_x + 2.0, min_y + 2.0, min_z),
            size=(w-4.0, (d/2)-3.0, 3.0),
            floor=0,
            room_type="living_room"
        )
        self.rooms[living.name] = living

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "house",
            "floors": self.floors,
            "footprint": self.footprint,
            "rooms": list(self.rooms.keys()),
        })
        return base