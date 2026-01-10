from dataclasses import dataclass, field
from typing import Tuple, Dict, Any, List
import numpy as np
import math

@dataclass
class ScoutBot:
    """
    Sensor scout: builds a 2D grid around center_xyz.
    mode: "sound" or "light"
    """
    name: str
    mode: str
    center_xyz: Tuple[float, float, float]
    extent_m: float = 40.0
    resolution_m: float = 2.0

    active: bool = True
    frames: int = 0

    grid: np.ndarray = field(default_factory=lambda: np.zeros((1, 1), dtype=float))
    peak_points_xy: List[Tuple[int, int]] = field(default_factory=list)

    def observe(self, world):
        if not self.active:
            return
        self.frames += 1

        cx, cy, cz = self.center_xyz
        r = float(self.extent_m)
        step = float(self.resolution_m)

        n = int((2*r) / step)
        n = max(8, min(128, n))
        grid = np.zeros((n, n), dtype=float)

        # Gather sources
        sources = []
        for place in world.places.values():
            if not hasattr(place, "rooms"):
                continue
            for room in place.rooms.values():
                if not hasattr(room, "objects"):
                    continue
                for obj in room.objects.values():
                    if self.mode == "sound" and hasattr(obj, "sound_level_at"):
                        sources.append(("sound", obj))
                    if self.mode == "light" and hasattr(obj, "light_level_at"):
                        sources.append(("light", obj))

        # Sample grid
        for iy in range(n):
            y = cy - r + iy * step
            for ix in range(n):
                x = cx - r + ix * step
                val = 0.0
                for _, obj in sources:
                    if self.mode == "sound":
                        val += obj.sound_level_at((x, y, cz))
                    else:
                        val += obj.light_level_at((x, y, cz))
                grid[iy, ix] = min(1.0, val)

        self.grid = grid

        # peak points for ledger (top K cells)
        flat = grid.flatten()
        if flat.size > 0:
            k = min(12, flat.size)
            idx = np.argpartition(flat, -k)[-k:]
            pts = []
            for i in idx:
                iy = int(i // n)
                ix = int(i % n)
                if grid[iy, ix] >= 0.25:
                    # map to 32x32 for SandySquare
                    gx = int((ix / max(1, n-1)) * 31)
                    gy = int((iy / max(1, n-1)) * 31)
                    pts.append((gx, gy))
            self.peak_points_xy = pts

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "scout",
            "name": self.name,
            "mode": self.mode,
            "frames": self.frames,
            "grid_shape": tuple(self.grid.shape),
            "peak_points_xy": self.peak_points_xy,
            "grid": self.grid,
        }