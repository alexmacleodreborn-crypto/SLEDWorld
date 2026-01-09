# world_core/scout_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, Dict, Any, List, Optional
import math

@dataclass
class ScoutBot:
    """
    Focused local sensor.
    signal in {"sound","light","shape"}.
    Produces a small 2D grid centered at center_xyz.
    """
    name: str
    signal: str
    center_xyz: Tuple[float, float, float]
    extent_m: float = 10.0
    resolution_m: float = 1.0
    max_frames: int = 50

    active: bool = True
    frames: int = 0
    grid: Optional[List[List[float]]] = None
    last_snapshot: Dict[str, Any] = field(default_factory=dict)

    def observe(self, world):
        if not self.active:
            return
        self.frames += 1
        if self.frames > self.max_frames:
            self.active = False
            return

        cx, cy, cz = self.center_xyz
        r = self.extent_m
        step = self.resolution_m
        n = int((2 * r) / step)

        grid = [[0.0 for _ in range(n)] for __ in range(n)]

        # gather sources: rooms + objects
        rooms = []
        for place in world.places.values():
            if hasattr(place, "rooms"):
                rooms.extend(list(place.rooms.values()))

        for iy in range(n):
            y = cy - r + iy * step
            for ix in range(n):
                x = cx - r + ix * step

                if self.signal == "shape":
                    # 1 if point is inside any room/place bounds (solid proxy)
                    solid = 0.0
                    for place in world.places.values():
                        if hasattr(place, "contains_world_point") and place.contains_world_point((x, y, cz)):
                            solid = 1.0
                            break
                    if solid == 0.0:
                        for room in rooms:
                            if room.contains_world_point((x, y, cz)):
                                solid = 1.0
                                break
                    grid[iy][ix] = solid

                elif self.signal in ("sound", "light"):
                    val = 0.0
                    for room in rooms:
                        # room returns aggregate
                        if self.signal == "sound":
                            src = getattr(room, "get_sound_level", lambda: 0.0)()
                        else:
                            src = getattr(room, "get_light_level", lambda: 0.0)()
                        if src <= 0:
                            continue

                        # approximate room center for attenuation
                        if room.bounds is None:
                            continue
                        (minx, miny, minz), (maxx, maxy, maxz) = room.bounds
                        rx = (minx + maxx) / 2
                        ry = (miny + maxy) / 2
                        rz = (minz + maxz) / 2
                        d = math.sqrt((x-rx)**2 + (y-ry)**2 + (cz-rz)**2)
                        att = 1.0 if d < 1.0 else 1.0 / (d**2)
                        att = max(att, 0.02)
                        val += src * att
                    grid[iy][ix] = round(min(val, 1.0), 3)

        self.grid = grid
        self.last_snapshot = {
            "source": "scout",
            "name": self.name,
            "signal": self.signal,
            "frame": getattr(world, "frame", self.frames),
            "active": self.active,
            "center_xyz": self.center_xyz,
            "resolution_m": step,
            "grid_size": n,
            "grid": grid,
        }

    def snapshot(self) -> Dict[str, Any]:
        return self.last_snapshot or {
            "source": "scout",
            "name": self.name,
            "signal": self.signal,
            "active": self.active,
            "frame": self.frames,
        }