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

        # World-space bounding box
        self.set_bounds(
            min_xyz=(x, y, z),
            max_xyz=(x + width, y + depth, z + height),
        )

        self.size = {
            "width": float(width),
            "depth": float(depth),
            "height": float(height),
        }

        self.floor = int(floor)
        self.room_type = room_type

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "room",
            "room_type": self.room_type,
            "floor": self.floor,
            "size": self.size,
        })
        return base