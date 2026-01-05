# world_core/profiles/room_profile.py

from world_core.world_object import WorldObject


class RoomProfile(WorldObject):
    """
    A room inside a house.
    Pure world-layer object with volume.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        size: tuple[float, float, float],  # (width, depth, height)
        floor: int,
        room_type: str,
    ):
        super().__init__(name=name, position=position)

        width, depth, height = size
        x, y, z = position

        # -----------------------------------------
        # World-space bounding box (explicit)
        # -----------------------------------------
        self.min_xyz = (
            float(x),
            float(y),
            float(z),
        )

        self.max_xyz = (
            float(x + width),
            float(y + depth),
            float(z + height),
        )

        # -----------------------------------------
        # Physical properties
        # -----------------------------------------
        self.size = {
            "width": float(width),
            "depth": float(depth),
            "height": float(height),
        }

        self.floor = int(floor)
        self.room_type = room_type

    # -----------------------------------------
    # Geometry test (CRITICAL)
    # -----------------------------------------

    def contains_world_point(self, xyz: tuple[float, float, float]) -> bool:
        x, y, z = xyz
        return (
            self.min_xyz[0] <= x <= self.max_xyz[0]
            and self.min_xyz[1] <= y <= self.max_xyz[1]
            and self.min_xyz[2] <= z <= self.max_xyz[2]
        )

    # -----------------------------------------
    # Observer snapshot
    # -----------------------------------------

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "room",
            "room_type": self.room_type,
            "floor": self.floor,
            "size": self.size,
            "bounds": {
                "min": self.min_xyz,
                "max": self.max_xyz,
            },
        })
        return base