import random
from world_core.world_object import WorldObject
from world_core.profiles.tv_profile import TVProfile
from world_core.profiles.remote_profile import RemoteProfile

class RoomProfile(WorldObject):
    def __init__(self, name, position, size, floor, room_type):
        super().__init__(name=name, position=position)
        width, depth, height = size
        x, y, z = position

        self.set_bounds(min_xyz=(x, y, z), max_xyz=(x+width, y+depth, z+height))
        self.size = {"width": float(width), "depth": float(depth), "height": float(height)}
        self.floor = int(floor)
        self.room_type = str(room_type)
        self.label = f"room:{self.room_type}"

        self.objects = {}
        self._build_objects()

    def _build_objects(self):
        if self.room_type == "living_room":
            (min_x, min_y, min_z), (max_x, max_y, _) = self.bounds

            # TV wall-mounted center of front wall
            tv_x = (min_x + max_x) / 2.0
            tv_y = min_y + 0.25
            tv_z = min_z + 1.5

            tv = TVProfile(name=f"{self.name}:tv", position=(tv_x, tv_y, tv_z))
            remote = RemoteProfile(
                name=f"{self.name}:remote",
                position=(tv_x - 0.8, tv_y + 1.0, min_z + 0.8),
                tv=tv,
            )

            self.objects["tv"] = tv
            self.objects["remote"] = remote

    def random_point_inside(self):
        (min_x, min_y, min_z), (max_x, max_y, max_z) = self.bounds
        return (
            random.uniform(min_x, max_x),
            random.uniform(min_y, max_y),
            random.uniform(min_z, max_z),
        )

    def interact(self, object_name: str, action: str):
        obj = self.objects.get(object_name)
        if obj is None:
            return False
        if hasattr(obj, action):
            return getattr(obj, action)()
        return False

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "room",
            "label": self.label,
            "room_type": self.room_type,
            "floor": self.floor,
            "size": self.size,
            "objects": {k: (v.snapshot() if hasattr(v, "snapshot") else str(v)) for k, v in self.objects.items()},
        })
        return base