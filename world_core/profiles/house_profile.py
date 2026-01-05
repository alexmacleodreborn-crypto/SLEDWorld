from world_core.world_object import WorldObject


class HouseProfile(WorldObject):
    """
    A residential house in the world.
    Pure world-layer object.

    Structure is spatial (XYZ), not symbolic.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        footprint: tuple[float, float],   # (width, depth) in meters
        floors: int = 2,
        residents: int = 3,
    ):
        # ✅ STANDARD: pass position as a single tuple
        super().__init__(name=name, position=position)

        # -----------------------------------------
        # Physical properties
        # -----------------------------------------
        self.footprint = footprint
        self.floors = floors
        self.residents = residents

        self.area = footprint[0] * footprint[1]

        # -----------------------------------------
        # Internal spatial layout (world-only)
        # Rooms are identified numerically, not linguistically
        # -----------------------------------------
        self.rooms = {
            0: {"type": "living",   "z": 0},
            1: {"type": "kitchen",  "z": 0},
            2: {"type": "bathroom", "z": 0},
            3: {"type": "bedroom",  "z": 1},
            4: {"type": "bedroom",  "z": 1},
            5: {"type": "toilet",   "z": 1},
        }

    # -----------------------------------------
    # OBSERVER VIEW
    # -----------------------------------------

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "house",
            "footprint": self.footprint,
            "area": self.area,
            "floors": self.floors,
            "residents": self.residents,
            "rooms": self.rooms,
        })
        return base