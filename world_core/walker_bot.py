# world_core/walker_bot.py

import random
from typing import Dict, Any

class WalkerBot:
    def __init__(self, name, start_xyz, world, return_interval=15):
        self.name = name
        self.world = world
        self.position = [float(start_xyz[0]), float(start_xyz[1]), float(start_xyz[2])]
        self.return_interval = int(return_interval)
        self._frame_last_toggle = 0
        self.last = {}

    def tick(self, clock):
        # simple random walk (v1)
        self.position[0] += random.uniform(-1.5, 1.5)
        self.position[1] += random.uniform(-1.5, 1.5)

        # every N frames: go “use remote”
        if (self.world.frame - self._frame_last_toggle) >= self.return_interval:
            self._frame_last_toggle = self.world.frame
            self._toggle_tv()

        # report
        self.last = {
            "source": "walker",
            "entity": self.name,
            "name": self.name,
            "frame": self.world.frame,
            "position_xyz": [round(self.position[0],2), round(self.position[1],2), round(self.position[2],2)],
            "heard_sound_level": self._read_living_room("sound_level"),
            "seen_light_level": self._read_living_room("light_level"),
            "seen_light_color": self._read_living_room("light_color"),
            "tv_state": self._read_tv_state(),
            "current_area": "world",
        }

    def _read_living_room(self, key: str):
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    rs = room.snapshot()
                    if rs.get("room_type") == "living_room":
                        return rs.get(key, 0.0)
        return 0.0

    def _read_tv_state(self):
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    rs = room.snapshot()
                    if rs.get("room_type") == "living_room":
                        tv = rs.get("objects", {}).get("tv")
                        if isinstance(tv, dict):
                            return tv.get("is_on")
        return None

    def _toggle_tv(self):
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.room_type == "living_room":
                        # use remote if exists
                        if "remote" in room.objects:
                            room.interact("remote", "power_toggle")
                        return

    def snapshot(self) -> Dict[str, Any]:
        return self.last or {"source":"walker","entity":self.name,"name":self.name,"frame":0}