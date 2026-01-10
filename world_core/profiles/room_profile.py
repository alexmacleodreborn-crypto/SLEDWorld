import random
from world_core.world_object import WorldObject
from world_core.profiles.tv_profile import TVProfile
from world_core.profiles.remote_profile import RemoteProfile


class RoomProfile(WorldObject):
    def __init__(self, name, position, size, floor, room_type):
        super().__init__(name=name, position=position)

        width, depth, height = size
        x, y, z = position

        self.set_bounds(min_xyz=(x, y, z), max_xyz=(x + width, y + depth, z + height))

        self.size = {"width": float(width), "depth": float(depth), "height": float(height)}
        self.floor = int(floor)
        self.room_type = str(room_type)
        self.label = f"room:{self.room_type}"

        self.objects = {}
        self._build_objects()

    def _build_objects(self):
        if self.room_type == "living_room":
            (min_x, min_y, min_z), (max_x, max_y, _) = self.bounds

            # wall-mounted center TV
            tv_x = (min_x + max_x) / 2.0
            tv_y = min_y + 0.5
            tv_z = min_z + 1.5

            tv = TVProfile(name=f"{self.name}:tv", position=(tv_x, tv_y, tv_z))
            remote = RemoteProfile(
                name=f"{self.name}:remote",
                position=(tv_x - 1.0, tv_y + 1.0, min_z + 0.8),
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

    def get_sound_level(self) -> float:
        total = 0.0
        for obj in self.objects.values():
            if hasattr(obj, "sound_level"):
                total += obj.sound_level()
        return round(min(total, 1.0), 3)

    def get_light_level(self) -> float:
        total = 0.0
        for obj in self.objects.values():
            if hasattr(obj, "light_level"):
                total += obj.light_level()
        return round(min(total, 1.0), 3)

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "room",
            "label": self.label,
            "room_type": self.room_type,
            "floor": self.floor,
            "size": self.size,
            "sound_level": self.get_sound_level(),
            "light_level": self.get_light_level(),
            "objects": {k: v.snapshot() for k, v in self.objects.items()},
        })
        return base