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
    - Contains physical objects (TV, Remote, etc.)
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
        CURRENT POLICY:
        - Every room has a TV
        - Every room has a Remote
        """

        (min_x, min_y, min_z), (max_x, max_y, _) = self.bounds

        # --- TV placement (wall-mounted) ---
        tv_x = (min_x + max_x) / 2.0
        tv_y = min_y + 0.4
        tv_z = min_z + 1.2

        tv = TVProfile(
            name=f"{self.name}:tv",
            position=(tv_x, tv_y, tv_z),
        )

        # --- Remote placement (table height, movable later) ---
        remote_x = tv_x + random.uniform(-0.5, 0.5)
        remote_y = tv_y + random.uniform(0.3, 0.8)
        remote_z = min_z + 0.8

        remote = RemoteProfile(
            name=f"{self.name}:remote",
            position=(remote_x, remote_y, remote_z),
            tv=tv,
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
            random.uniform(min_y, max_y),
            random.uniform(min_z, max_z),
        )

    # =================================================
    # Environmental outputs
    # =================================================

    def get_sound_level(self) -> float:
        """
        Aggregate sound level from all objects in the room.
        """
        total = 0.0
        for obj in self.objects.values():
            if hasattr(obj, "sound_level"):
                total += obj.sound_level()
        return round(min(total, 1.0), 2)

    # =================================================
    # Interaction surface
    # =================================================

    def interact(self, object_name: str, action: str) -> bool:
        obj = self.objects.get(object_name)
        if obj is None:
            return False

        if hasattr(obj, action):
            getattr(obj, action)()
            return True

        return False

    # =================================================
    # Observer snapshot
    # =================================================

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "room",
            "label": self.label,
            "room_type": self.room_type,
            "floor": self.floor,
            "size": self.size,
            "sound_level": self.get_sound_level(),
            "objects": {
                name: obj.snapshot()
                for name, obj in self.objects.items()
            },
        })
        return base