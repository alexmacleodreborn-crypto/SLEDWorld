from dataclasses import dataclass, field
from typing import Dict, Tuple, Any, List
import numpy as np

@dataclass
class SurveyorBot:
    """
    3D geometry surveyor (lightweight).
    Produces a 2D surface slice + a small list of surface points for the ledger.
    """
    name: str
    center_xyz: Tuple[float, float, float]
    extent_m: float = 40.0
    resolution_m: float = 2.0
    height_m: float = 8.0

    active: bool = True
    frames: int = 0

    _surface_slice: np.ndarray = field(default_factory=lambda: np.zeros((1, 1), dtype=float))
    _surface_points_xy: List[Tuple[int, int]] = field(default_factory=list)
    last_snapshot: Dict[str, Any] = field(default_factory=dict)

    def _is_solid(self, world, x, y, z) -> bool:
        for place in world.places.values():
            if hasattr(place, "contains_world_point") and place.contains_world_point((x, y, z)):
                return True
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point((x, y, z)):
                        return True
        return False

    def observe(self, world):
        if not self.active:
            return
        self.frames += 1

        cx, cy, cz = self.center_xyz
        r = float(self.extent_m)
        step = float(self.resolution_m)

        n = int((2*r) / step)
        n = max(8, min(128, n))
        z = cz + 1.0  # sample at ~human height

        surf = np.zeros((n, n), dtype=float)

        # Mark solid vs air on slice
        for iy in range(n):
            y = cy - r + iy * step
            for ix in range(n):
                x = cx - r + ix * step
                surf[iy, ix] = 1.0 if self._is_solid(world, x, y, z) else 0.0

        self._surface_slice = surf

        # Extract a small set of boundary points (surface points)
        pts = []
        for iy in range(1, n-1):
            for ix in range(1, n-1):
                if surf[iy, ix] == 1.0:
                    if (
                        surf[iy-1, ix] == 0.0 or surf[iy+1, ix] == 0.0 or
                        surf[iy, ix-1] == 0.0 or surf[iy, ix+1] == 0.0
                    ):
                        gx = int((ix / max(1, n-1)) * 31)
                        gy = int((iy / max(1, n-1)) * 31)
                        pts.append((gx, gy))

        # keep small
        self._surface_points_xy = pts[:80]

        self.last_snapshot = {
            "source": "surveyor",
            "name": self.name,
            "frame": getattr(world, "frame", self.frames),
            "active": self.active,
            "center_xyz": self.center_xyz,
            "resolution_m": step,
            "surface_points_xy": self._surface_points_xy,
            "surface_shape": tuple(self._surface_slice.shape),
        }

    def surface_slice_2d(self):
        return self._surface_slice if self._surface_slice.size else None

    def snapshot(self) -> Dict[str, Any]:
        return self.last_snapshot or {
            "source": "surveyor",
            "name": self.name,
            "active": self.active,
            "frame": self.frames,
        }