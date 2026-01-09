# world_core/profiles/hospital_profile.py

from __future__ import annotations
from world_core.world_object import WorldObject
from world_core.profiles.room_profile import RoomProfile

class HospitalProfile(WorldObject):
    def __init__(self, name, position, footprint=(30.0, 20.0), floors=1):
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
        # simple: reception + corridor
        reception = RoomProfile(
            name=f"{self.name}:reception",
            position=(x + 1.0, y + 1.0, z),
            size=(w/2 - 2.0, d - 2.0, 3.0),
            floor=0,
            room_type="reception",
        )
        corridor = RoomProfile(
            name=f"{self.name}:corridor",
            position=(x + w/2, y + 1.0, z),
            size=(w/2 - 1.0, d - 2.0, 3.0),
            floor=0,
            room_type="corridor",
        )
        self.rooms[reception.name] = reception
        self.rooms[corridor.name] = corridor

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "hospital",
            "footprint": self.footprint,
            "floors": self.floors,
            "rooms": list(self.rooms.keys()),
        })
        return base