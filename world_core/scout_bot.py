# world_core/scout_bot.py

import math
from dataclasses import dataclass, field
from typing import Any, Dict, Tuple, List

@dataclass
class ScoutBot:
    name: str
    mode: str                     # "sound" or "light"
    center_xyz: Tuple[float,float,float]
    extent_m: float = 25.0
    resolution_m: float = 2.0
    max_frames: int = 999999

    active: bool = True
    frames: int = 0
    grid: List[List[float]] = field(default_factory=list)
    last_snapshot: Dict[str, Any] = field(default_factory=dict)

    def observe(self, world):
        if not self.active:
            return
        self.frames += 1
        if self.frames > self.max_frames:
            self.active = False
            return

        cx, cy, cz = self.center_xyz
        r = float(self.extent_m)
        step = float(self.resolution_m)

        n = int((2*r)/step) or 1
        out = [[0.0 for _ in range(n)] for __ in range(n)]

        # sample room sources as point emitters (simple)
        sources = []
        for place in world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    rs = room.snapshot()
                    lvl = rs.get("sound_level") if self.mode == "sound" else rs.get("light_level")
                    if lvl and lvl > 0:
                        # use room center
                        (minx,miny,minz),(maxx,maxy,maxz) = room.bounds
                        sx = (minx+maxx)/2
                        sy = (miny+maxy)/2
                        sz = (minz+maxz)/2
                        sources.append((sx,sy,sz,float(lvl)))

        for iy in range(n):
            y = cy - r + iy*step
            for ix in range(n):
                x = cx - r + ix*step
                total = 0.0
                for (sx,sy,sz,lvl) in sources:
                    dx = x - sx
                    dy = y - sy
                    dz = cz - sz
                    d2 = dx*dx + dy*dy + dz*dz
                    if d2 < 1.0:
                        att = 1.0
                    else:
                        att = 1.0 / d2
                    att = max(att, 0.02)
                    total += lvl * att
                out[iy][ix] = round(min(total, 1.0), 3)

        self.grid = out
        self.last_snapshot = {
            "source": "scout",
            "entity": self.name,
            "name": self.name,
            "mode": self.mode,
            "frame": world.frame,
            "active": self.active,
            "center_xyz": self.center_xyz,
            "extent_m": self.extent_m,
            "resolution_m": self.resolution_m,
            "summary": {
                "max": max(max(row) for row in out) if out else 0.0,
                "mean": round(sum(sum(row) for row in out) / max(1, (n*n)), 3),
            },
            "grid": out,
        }

    def snapshot(self):
        return self.last_snapshot or {"source":"scout","entity":self.name,"name":self.name,"mode":self.mode,"active":self.active,"frame":self.frames}