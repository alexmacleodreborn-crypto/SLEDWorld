# world_core/scout_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import math


def _dist(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)


@dataclass
class ScoutBot:
    """
    Stakeout scout.
    - Watches one target zone for N frames
    - Records sound + light fields
    - Emits simple “shape grid” placeholder (later replaced by surface scanning)
    """
    name: str
    target_room: Optional[str] = None
    target_object: Optional[str] = None
    radius_m: float = 8.0
    max_frames: int = 50

    active: bool = True
    frames: int = 0

    # data capture
    sound_series: List[float] = field(default_factory=list)
    light_series: List[float] = field(default_factory=list)
    darkness_series: List[float] = field(default_factory=list)

    # shape placeholders
    grid_size: int = 16
    resolution: int = 1

    last_snapshot: Dict[str, Any] = field(default_factory=dict)

    def _find_target_xyz(self, world) -> Optional[Tuple[float, float, float]]:
        # If targeting object, try locate it
        if self.target_room:
            for place in world.places.values():
                if hasattr(place, "rooms"):
                    for room in place.rooms.values():
                        if room.name == self.target_room:
                            # center of room bounds if present
                            bounds = getattr(room, "bounds", None)
                            if bounds:
                                (minx, miny, minz), (maxx, maxy, maxz) = bounds
                                return ((minx+maxx)/2, (miny+maxy)/2, (minz+maxz)/2)
                            if hasattr(room, "position"):
                                return tuple(room.position)

        # fallback: if object target exists
        if self.target_object:
            for place in world.places.values():
                if hasattr(place, "rooms"):
                    for room in place.rooms.values():
                        if hasattr(room, "objects") and self.target_object in room.objects:
                            obj = room.objects[self.target_object]
                            if hasattr(obj, "position"):
                                return tuple(obj.position)

        return None

    def _measure_sound(self, world, target_xyz: Optional[Tuple[float, float, float]]) -> float:
        """
        Simple: sum room sound levels with inverse-distance attenuation from target point.
        """
        if target_xyz is None:
            return 0.0

        total = 0.0
        tx, ty, tz = target_xyz

        for place in world.places.values():
            if not hasattr(place, "rooms"):
                continue
            for room in place.rooms.values():
                # room sound if method exists
                lvl = 0.0
                if hasattr(room, "get_sound_level"):
                    try:
                        lvl = float(room.get_sound_level())
                    except Exception:
                        lvl = 0.0

                if lvl <= 0:
                    continue

                # distance from room center
                bounds = getattr(room, "bounds", None)
                if bounds:
                    (minx, miny, minz), (maxx, maxy, maxz) = bounds
                    cx, cy, cz = (minx+maxx)/2, (miny+maxy)/2, (minz+maxz)/2
                else:
                    if hasattr(room, "position"):
                        cx, cy, cz = room.position
                    else:
                        continue

                d = math.sqrt((tx-cx)**2 + (ty-cy)**2 + (tz-cz)**2)
                if d < 1.0:
                    atten = 1.0
                else:
                    atten = 1.0 / (d*d)
                atten = max(atten, 0.02)
                total += lvl * atten

        return round(min(total, 1.0), 3)

    def _measure_light(self, world) -> Tuple[float, float]:
        """
        Global light from WorldSpace for now.
        Later: add object-emission lights (TV glow etc).
        """
        space = getattr(world, "space", None)
        if space and hasattr(space, "state"):
            light = float(getattr(space.state, "ambient_light", 0.5))
            darkness = float(getattr(space.state, "darkness", 0.5))
            return (round(light, 3), round(darkness, 3))
        return (0.5, 0.5)

    def observe(self, world):
        if not self.active:
            return

        self.frames += 1
        if self.frames > self.max_frames:
            self.active = False
            return

        target_xyz = self._find_target_xyz(world)

        sound = self._measure_sound(world, target_xyz)
        light, dark = self._measure_light(world)

        self.sound_series.append(sound)
        self.light_series.append(light)
        self.darkness_series.append(dark)

        # minimal placeholder shape grid: all zeros until you wire surface scanning
        # (still included so Streamlit always has something to render)
        shape_grid = [[0 for _ in range(self.grid_size)] for __ in range(self.grid_size)]

        frame = getattr(getattr(world, "space", None), "frame_counter", self.frames)

        self.last_snapshot = {
            "source": "scout",
            "name": self.name,
            "type": "scout",
            "active": bool(self.active),
            "frame": int(frame),
            "frames": int(self.frames),
            "grid_size": int(self.grid_size),
            "resolution": int(self.resolution),

            "target_room": self.target_room,
            "target_object": self.target_object,
            "radius_m": float(self.radius_m),

            "sound_now": sound,
            "light_now": light,
            "darkness_now": dark,

            "sound_series_tail": self.sound_series[-10:],
            "light_series_tail": self.light_series[-10:],
            "darkness_series_tail": self.darkness_series[-10:],

            # safe optional key so your UI won’t KeyError
            "shape_persistence": 0,

            "shape_grid": shape_grid,
        }

    def snapshot(self) -> Dict[str, Any]:
        return self.last_snapshot or {
            "source": "scout",
            "name": self.name,
            "type": "scout",
            "active": self.active,
            "frames": self.frames,
            "shape_persistence": 0,
        }