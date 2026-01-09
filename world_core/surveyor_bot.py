# world_core/surveyor_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Tuple
import math


@dataclass
class SurveyorBot:
    """
    Geometry surveyor.

    Purpose:
    - Map solid vs empty space
    - Detect surfaces (solid ↔ empty boundaries)
    - No interaction
    - No semantics
    - No time awareness

    Output:
    - occupancy_grid (0 empty, 1 solid)
    - surface_grid (1 surface voxel)
    """

    name: str
    center_xyz: Tuple[float, float, float]
    extent_m: float = 6.0        # radius around center
    resolution_m: float = 0.5    # voxel size
    max_frames: int = 50

    active: bool = True
    frames: int = 0

    occupancy_grid: list = field(default_factory=list)
    surface_grid: list = field(default_factory=list)

    last_snapshot: Dict[str, Any] = field(default_factory=dict)

    # -------------------------------------------------
    # Geometry helpers
    # -------------------------------------------------

    def _is_solid(self, world, x, y, z) -> bool:
        """
        Check if point lies inside any world object bounds.
        """
        for place in world.places.values():
            # place volume
            if hasattr(place, "contains_world_point"):
                if place.contains_world_point((x, y, z)):
                    return True

            # room volumes
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point((x, y, z)):
                        return True

                    # object volumes
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

        # 2D slice at center Z (intentional simplicity)
        for ix in range(size):
            for iy in range(size):
                x = cx - r + ix * step
                y = cy - r + iy * step
                z = cz

                if self._is_solid(world, x, y, z):
                    occ[iy][ix] = 1

        # Surface detection (simple edge detection)
        surf = [[0 for _ in range(size)] for __ in range(size)]
        for y in range(1, size - 1):
            for x in range(1, size - 1):
                if occ[y][x] == 1:
                    neighbors = (
                        occ[y-1][x], occ[y+1][x],
                        occ[y][x-1], occ[y][x+1],
                    )
                    if any(n == 0 for n in neighbors):
                        surf[y][x] = 1

        self.occupancy_grid = occ
        self.surface_grid = surf

        frame = getattr(getattr(world, "space", None), "frame_counter", self.frames)

        self.last_snapshot = {
            "source": "surveyor",
            "name": self.name,
            "frame": frame,
            "active": self.active,
            "center_xyz": self.center_xyz,
            "extent_m": self.extent_m,
            "resolution_m": self.resolution_m,
            "grid_size": size,
            "occupancy_grid": occ,
            "surface_grid": surf,
        }

    def snapshot(self) -> Dict[str, Any]:
        return self.last_snapshot or {
            "source": "surveyor",
            "name": self.name,
            "active": self.active,
        }