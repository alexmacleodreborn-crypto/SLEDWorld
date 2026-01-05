# world_core/profiles/house_profile.py

from world_core.world_object import WorldObject
from world_core.profiles.room_profile import RoomProfile


class HouseProfile(WorldObject):
    """
    A residential house in the world.
    Pure world-layer object.
    """

    FLOOR_HEIGHT = 2500.0  # meters (abstract world scale)

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        footprint: tuple[float, float],   # (width, depth)
        residents: int = 3,
        floors: int = 2,
    ):
        super().__init__(name=name, position=position)

        self.footprint = (float(footprint[0]), float(footprint[1]))
        self.residents = int(residents)
        self.floors = int(floors)

        self.area = self.footprint[0] * self.footprint[1]
        self.height = self.floors * self.FLOOR_HEIGHT

        # Define house bounds in WORLD space
        x, y, z = self.position
        self.set_bounds(
            min_xyz=(x, y, z),
            max_xyz=(
                x + self.footprint[0],
                y + self.footprint[1],
                z + self.height,
            ),
        )

        # -----------------------------------------
        # Rooms (real volumetric objects)
        # -----------------------------------------
        self.rooms: dict[int, RoomProfile] = {}
        self._build_rooms()

    # =================================================
    # Room construction
    # =================================================

    def _build_rooms(self):
        """
        Build 6 rooms across floors with real XYZ volumes.
        """

        room_defs = [
            (0, "living_room"),
            (0, "kitchen"),
            (0, "bathroom"),
            (1, "bedroom_1"),
            (1, "bedroom_2"),
            (1, "bedroom_3"),
        ]

        room_width = self.footprint[0] / 3.0
        room_depth = self.footprint[1] / 2.0
        room_height = self.FLOOR_HEIGHT

        base_x, base_y, base_z = self.position

        index = 0
        for floor, room_type in room_defs:
            col = index % 3
            row = (index // 3) % 2

            x = base_x + col * room_width
            y = base_y + row * room_depth
            z = base_z + floor * self.FLOOR_HEIGHT

            room = RoomProfile(
                name=f"{self.name}:{room_type}",
                position=(x, y, z),
                size=(room_width, room_depth, room_height),
                floor=floor,
                room_type=room_type,
            )

            self.rooms[index] = room
            index += 1

    # =================================================
    # Observer snapshot
    # =================================================

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "house",
            "footprint": list(self.footprint),
            "area": self.area,
            "residents": self.residents,
            "floors": self.floors,
            "height": self.height,
            "rooms": {
                idx: room.snapshot()
                for idx, room in self.rooms.items()
            },
        })
        return base