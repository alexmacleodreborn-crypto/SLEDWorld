from world_core.world_object import WorldObject
import random


class HouseProfile(WorldObject):
    """
    A residential house with internal spatial rooms.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        footprint: tuple[float, float],   # (width, depth)
        floors: int = 2,
        residents: int = 3,
    ):
        x, y, z = position
        super().__init__(name, x, y, z)

        self.footprint = footprint
        self.floors = floors
        self.residents = residents
        self.area = footprint[0] * footprint[1]

        # ---------------------------------
        # Room layout (LOCAL offsets)
        # ---------------------------------
        w, d = footprint

        self.rooms = {
            0: {"type": "living",   "box": (0,     0,     0, w/2, d/2, 3)},
            1: {"type": "kitchen",  "box": (w/2,   0,     0, w,   d/2, 3)},
            2: {"type": "bathroom", "box": (0,     d/2,   0, w/2, d,   3)},
            3: {"type": "bedroom",  "box": (0,     0,     3, w/2, d/2, 6)},
            4: {"type": "bedroom",  "box": (w/2,   0,     3, w,   d/2, 6)},
            5: {"type": "toilet",   "box": (0,     d/2,   3, w/2, d,   6)},
        }

    # ---------------------------------
    # Spatial helpers
    # ---------------------------------

    def random_point_in_room(self, room_id: int):
        room = self.rooms[room_id]["box"]
        x1, y1, z1, x2, y2, z2 = room

        return (
            self.position[0] + random.uniform(x1, x2),
            self.position[1] + random.uniform(y1, y2),
            random.uniform(z1, z2),
        )

    # ---------------------------------
    # Snapshot
    # ---------------------------------

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "house",
            "footprint": self.footprint,
            "area": self.area,
            "floors": self.floors,
            "residents": self.residents,
            "rooms": {
                k: {"type": v["type"], "box": v["box"]}
                for k, v in self.rooms.items()
            },
        })
        return base