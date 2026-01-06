# world_core/profiles/room_profile.py

import random
from world_core.world_object import WorldObject


class RoomProfile(WorldObject):
    """
    A room inside a house.

    Rules:
    - Pure world-layer object
    - Real 3D volume in WORLD coordinates
    - No agents
    - No cognition
    - No time
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
        # World-space bounding box (AUTHORITATIVE)
        # -----------------------------------------
        self.set_bounds(
            min_xyz=(x, y, z),
            max_xyz=(x + width, y + depth, z + height),
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
        self.room_type = str(room_type)

        # Canonical semantic label
        self.label = f"room:{self.room_type}"

    # =================================================
    # Spatial helpers (CRITICAL for walkers)
    # =================================================

    def random_point_inside(self) -> tuple[float, float, float]:
        """
        Return a random WORLD-space point inside this room.
        Used for movement targets.
        """
        (min_x, min_y, min_z), (max_x, max_y, max_z) = self.bounds

        return (
            random.uniform(min_x, max_x),
            random.uniform(min_y, max_y),
            random.uniform(min_z, max_z),
        )

    # -----------------------------------------
    # Observer snapshot
    # -----------------------------------------

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "room",
            "label": self.label,
            "room_type": self.room_type,
            "floor": self.floor,
            "size": self.size,
        })
        return base