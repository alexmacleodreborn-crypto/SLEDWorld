from dataclasses import dataclass, field
from typing import Dict, Tuple, Any, List


@dataclass
class SurveyorBot:
    name: str
    center_xyz: Tuple[float, float, float]
    extent_m: float = 10.0
    resolution_m: float = 1.0
    height_m: float = 6.0
    max_frames: int = 999999

    active: bool = True
    frames: int = 0

    volume: List[List[List[int]]] = field(default_factory=list)
    surface_volume: List[List[List[int]]] = field(default_factory=list)
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
        if self.frames > self.max_frames:
            self.active = False
            return

        cx, cy, cz = self.center_xyz
        r = self.extent_m
        step = self.resolution_m
        h = self.height_m

        nx = int((2 * r) / step)
        ny = nx
        nz = int(h / step)
        nx = max(nx, 1)
        ny = max(ny, 1)
        nz = max(nz, 1)

        vol = [[[0 for _ in range(nx)] for __ in range(ny)] for ___ in range(nz)]

        for iz in range(nz):
            z = cz + iz * step
            for iy in range(ny):
                y = cy - r + iy * step
                for ix in range(nx):
                    x = cx - r + ix * step
                    if self._is_solid(world, x, y, z):
                        vol[iz][iy][ix] = 1

        surf = [[[0 for _ in range(nx)] for __ in range(ny)] for ___ in range(nz)]
        if nz >= 3 and nx >= 3 and ny >= 3:
            for z in range(1, nz - 1):
                for y in range(1, ny - 1):
                    for x in range(1, nx - 1):
                        if vol[z][y][x] == 1:
                            if (
                                vol[z-1][y][x] == 0 or vol[z+1][y][x] == 0 or
                                vol[z][y-1][x] == 0 or vol[z][y+1][x] == 0 or
                                vol[z][y][x-1] == 0 or vol[z][y][x+1] == 0
                            ):
                                surf[z][y][x] = 1

        frame = getattr(world.space, "frame_counter", self.frames)

        self.volume = vol
        self.surface_volume = surf
        self.last_snapshot = {
            "source": "surveyor",
            "name": self.name,
            "frame": frame,
            "active": self.active,
            "center_xyz": self.center_xyz,
            "resolution_m": step,
            "volume_shape": (nz, ny, nx),
            "volume": vol,
            "surface_volume": surf,
        }

    def snapshot(self) -> Dict[str, Any]:
        return self.last_snapshot or {
            "source": "surveyor",
            "name": self.name,
            "active": self.active,
            "frame": self.frames,
        }