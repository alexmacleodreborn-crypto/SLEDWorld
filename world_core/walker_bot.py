import math
import random

class WalkerBot:
    """
    Physical walker. Returns to living room TV every return_interval frames and toggles it.
    Emits: position, area, last_interaction, points_xy (coarse).
    """
    def __init__(self, name, start_xyz, world, return_interval=15):
        self.name = name
        self.world = world
        self.return_interval = int(return_interval)

        self.position = [float(start_xyz[0]), float(start_xyz[1]), float(start_xyz[2])]
        self.speed_m_per_min = 2.0
        self.current_area = "world"
        self.last_interaction = None

        self._frame_counter = 0

    def tick(self, clock):
        self._frame_counter += 1
        self.last_interaction = None

        # Every N frames: go to TV and toggle it (guaranteed signal)
        if self._frame_counter % self.return_interval == 0:
            self._try_toggle_tv()
        else:
            # otherwise random wander small
            self._wander()

        self._resolve_current_area()

    def _wander(self):
        # small random walk
        self.position[0] += random.uniform(-1.0, 1.0)
        self.position[1] += random.uniform(-1.0, 1.0)

    def _try_toggle_tv(self):
        # Find any room with tv+remote, toggle remote power
        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue
            for room in place.rooms.values():
                if getattr(room, "room_type", "") != "living_room":
                    continue
                if not hasattr(room, "objects"):
                    continue
                if "remote" in room.objects:
                    # move to room center-ish
                    (min_x, min_y, min_z), (max_x, max_y, max_z) = room.bounds
                    self.position[0] = (min_x + max_x) / 2
                    self.position[1] = (min_y + max_y) / 2
                    self.position[2] = (min_z + max_z) / 2

                    room.interact("remote", "power_toggle")
                    self.last_interaction = "remote:power_toggle"
                    return

    def _resolve_current_area(self):
        xyz = tuple(self.position)
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point(xyz):
                        self.current_area = room.name
                        return
        for place in self.world.places.values():
            if place.contains_world_point(xyz):
                self.current_area = place.name
                return
        self.current_area = "world"

    def snapshot(self):
        # Coarse point for SandySquare (map to 32x32)
        px = int((self.position[0] % 64) / 2)
        py = int((self.position[1] % 64) / 2)
        return {
            "source": "walker",
            "name": self.name,
            "frame": getattr(self.world, "frame", 0),
            "position_xyz": [round(v, 2) for v in self.position],
            "current_area": self.current_area,
            "speed_m_per_min": self.speed_m_per_min,
            "last_interaction": self.last_interaction,
            "points_xy": [(px, py)] if self.last_interaction else [],
        }