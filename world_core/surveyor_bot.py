# world_core/surveyor_bot.py

from dataclasses import dataclass, field
from typing import Dict, Tuple, Any


@dataclass
class SurveyorBot:
    """
    Pure geometry surveyor.

    - Detects solid vs empty space
    - Detects surfaces (solid boundaries)
    - No interaction
    - No semantics
    - No time awareness
    """

    name: str
    center_xyz: Tuple[float, float, float]
    extent_m: float = 6.0
    resolution_m: float = 0.5
    max_frames: int = 50

    active: bool = True
    frames: int = 0

    occupancy_grid: list = field(default_factory=list)
    surface_grid: list = field(default_factory=list)
    last_snapshot: Dict[str, Any] = field(default_factory=dict)

    # -------------------------------------------------
    # Geometry query
    # -------------------------------------------------

    def _is_solid(self, world, x, y, z) -> bool:
        for place in world.places.values():
            if hasattr(place, "contains_world_point"):
                if place.contains_world_point((x, y, z)):
                    return True

            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point((x, y, z)):
                        return True

                    if hasattr(room, "objects"):
                        for obj in room.objects.values():
                            if hasattr(obj, "contains_world_point"):
                                if obj.contains_world_point((x, y, z)):
                                    return True
        return False

    # -------------------------------------------------
    # Survey step
    # -------------------------------------------------

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

        size = int((2 * r) / step)
        occ = [[0 for _ in range(size)] for __ in range(size)]

        # 2D slice at Z = center (intentional)
        for ix in range(size):
            for iy in range(size):
                x = cx - r + ix * step
                y = cy - r + iy * step
                z = cz

                if self._is_solid(world, x, y, z):
                    occ[iy][ix] = 1

        surf = [[0 for _ in range(size)] for __ in range(size)]
        for y in range(1, size - 1):
            for x in range(1, size - 1):
                if occ[y][x] == 1:
                    if (
                        occ[y - 1][x] == 0
                        or occ[y + 1][x] == 0
                        or occ[y][x - 1] == 0
                        or occ[y][x + 1] == 0
                    ):
                        surf[y][x] = 1

        self.occupancy_grid = occ
        self.surface_grid = surf

        self.last_snapshot = {
            "source": "surveyor",
            "name": self.name,
            "frame": self.frames,
            "center_xyz": self.center_xyz,
            "extent_m": self.extent_m,
            "resolution_m": self.resolution_m,
            "occupancy_grid": occ,
            "surface_grid": surf,
            "active": self.active,
        }

    def snapshot(self):
        return self.last_snapshot