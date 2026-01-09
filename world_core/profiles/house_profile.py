# world_core/profiles/house_profile.py

from __future__ import annotations
from world_core.world_object import WorldObject
from world_core.profiles.room_profile import RoomProfile

class HouseProfile(WorldObject):
    def __init__(self, name, position, footprint=(20.0, 14.0), floors=1):
        super().__init__(name=name, position=position)
        self.footprint = footprint
        self.floors = int(floors)

        x, y, z = position
        w, d = footprint
        self.set_bounds((x, y, z), (x + w, y + d, z + 4.0))

        self.rooms = {}
        self._build_rooms()

    def _build_rooms(self):
        x, y, z = self.position
        w, d = self.footprint

        living = RoomProfile(
            name=f"{self.name}:living_room",
            position=(x + 1.0, y + 1.0, z),
            size=(w - 2.0, d/2 - 1.5, 3.0),
            floor=0,
            room_type="living_room",
        )
        bedroom = RoomProfile(
            name=f"{self.name}:bedroom",
            position=(x + 1.0, y + d/2, z),
            size=(w - 2.0, d/2 - 1.5, 3.0),
            floor=0,
            room_type="bedroom",
        )
        self.rooms[living.name] = living
        self.rooms[bedroom.name] = bedroom

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "house",
            "footprint": self.footprint,
            "floors": self.floors,
            "rooms": list(self.rooms.keys()),
        })
        return base