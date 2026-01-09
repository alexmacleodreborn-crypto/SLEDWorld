# world_core/scout_bot.py

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


@dataclass
class ScoutBot:
    """
    Stakeout scout:
    Watches a target room/object for N frames and records fields.
    """

    name: str
    target_room_type: str = "living_room"
    target_object_key: str = "tv"
    max_frames: int = 50

    active: bool = True
    frames: int = 0

    sound_series: List[float] = field(default_factory=list)
    light_intensity_series: List[float] = field(default_factory=list)
    light_color_series: List[str] = field(default_factory=list)

    last_snapshot: Dict[str, Any] = field(default_factory=dict)

    def _find_target(self, world):
        for place in world.places.values():
            if not hasattr(place, "rooms"):
                continue
            for room in place.rooms.values():
                if getattr(room, "room_type", "") != self.target_room_type:
                    continue
                obj = getattr(room, "objects", {}).get(self.target_object_key)
                if obj:
                    return room, obj
        return None, None

    def observe(self, world):
        if not self.active:
            return

        self.frames += 1
        if self.frames > self.max_frames:
            self.active = False
            return

        frame = int(getattr(getattr(world, "space", None), "frame_counter", self.frames))

        room, obj = self._find_target(world)
        sound = 0.0
        light_int = 0.0
        light_color = "none"

        if room and hasattr(room, "get_sound_level"):
            try:
                sound = float(room.get_sound_level())
            except Exception:
                sound = 0.0

        if obj and hasattr(obj, "get_light_output"):
            try:
                lo = obj.get_light_output()
                light_int = float(lo.get("intensity", 0.0))
                light_color = lo.get("color", "none")
            except Exception:
                pass

        self.sound_series.append(round(sound, 3))
        self.light_intensity_series.append(round(light_int, 3))
        self.light_color_series.append(light_color)

        self.last_snapshot = {
            "source": "scout",
            "name": self.name,
            "frame": frame,
            "active": self.active,
            "target_room_type": self.target_room_type,
            "target_object_key": self.target_object_key,
            "sound_now": round(sound, 3),
            "light_now": {"intensity": round(light_int, 3), "color": light_color},
            "sound_tail": self.sound_series[-25:],
            "light_intensity_tail": self.light_intensity_series[-25:],
            "light_color_tail": self.light_color_series[-25:],
        }

    def snapshot(self) -> Dict[str, Any]:
        return self.last_snapshot or {
            "source": "scout",
            "name": self.name,
            "active": self.active,
            "frame": self.frames,
        }