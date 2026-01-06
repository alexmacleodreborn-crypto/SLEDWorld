# world_core/profiles/room_profile.py

import random
from world_core.world_object import WorldObject
from world_core.profiles.tv_profile import TVProfile
from world_core.profiles.remote_profile import RemoteProfile


class RoomProfile(WorldObject):
    """
    A room inside a house.

    Rules:
    - Pure world-layer object
    - Real 3D volume in WORLD coordinates
    - Contains physical objects (TV, remote, etc.)
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

        # -----------------------------------------
        # Physical objects inside the room
        # -----------------------------------------
        self.objects: dict[str, WorldObject] = {}
        self._build_objects()

    # =================================================
    # Object construction
    # =================================================

    def _build_objects(self):
        """
        Populate room with physical objects.
        """
        if self.room_type == "living_room":
            (min_x, min_y, min_z), (max_x, max_y, _) = self.bounds

            # --------------------
            # TV (fixed)
            # --------------------
            tv_x = (min_x + max_x) / 2.0
            tv_y = min_y + 0.5
            tv_z = min_z + 1.0

            tv = TVProfile(
                name=f"{self.name}:tv",
                position=(tv_x, tv_y, tv_z),
            )

            # --------------------
            # Remote (portable, bound to TV)
            # --------------------
            remote = RemoteProfile(
                name=f"{self.name}:remote",
                position=(
                    tv_x - 1.0,
                    tv_y + 1.0,
                    min_z + 0.8,
                ),
                tv=tv,  # binds remote → TV
            )

            self.objects["tv"] = tv
            self.objects["remote"] = remote

    # =================================================
    # Spatial helpers
    # =================================================

    def random_point_inside(self) -> tuple[float, float, float]:
        (min_x, min_y, min_z), (max_x, max_y, max_z) = self.bounds
        return (
            random.uniform(min_x, max_x),
            random.uniform(min_y,