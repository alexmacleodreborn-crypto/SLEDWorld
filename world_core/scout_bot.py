# world_core/scout_bot.py

import math
import numpy as np


class ScoutBot:
    """
    Ephemeral perception probe.

    Purpose:
    - Stake out a region of space
    - Record local shape (occupancy)
    - Record sound/light intensity as fields
    - NO movement
    - NO cognition
    - NO decisions

    Scouts exist for a fixed number of frames,
    then terminate.
    """

    def __init__(
        self,
        name: str,
        center_xyz: tuple[float, float, float],
        grid_size: int = 16,
        resolution: float = 1.0,
        max_frames: int = 300,
    ):
        self.name = name
        self.type = "scout"

        self.center_xyz = np.array(center_xyz, dtype=float)

        self.grid_size = grid_size
        self.resolution = resolution
        self.max_frames = max_frames

        self.frame = 0
        self.active = True

        # ---------------------------------
        # Perception grids
        # ---------------------------------
        self.occupancy = np.zeros((grid_size, grid_size))
        self.sound = np.zeros((grid_size, grid_size))

        # Persistence metric (very early objectness)
        self.shape_persistence = 0

    # =================================================
    # OBSERVE WORLD
    # =================================================

    def observe(self, world):
        if not self.active:
            return

        self.frame += 1

        self._sense_geometry(world)
        self._sense_sound(world)

        if self.frame >= self.max_frames:
            self.active = False

    # =================================================
    # GEOMETRY / SHAPE
    # =================================================

    def _sense_geometry(self, world):
        """
        Marks occupied cells based on world places.
        """
        cx, cy, _ = self.center_xyz

        half = self.grid_size // 2

        new_occ = np.zeros_like(self.occupancy)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                wx = cx + (i - half) * self.resolution
                wy = cy + (j - half) * self.resolution
                wz = 0.0

                for place in world.places.values():
                    if place.contains_world_point((wx, wy, wz)):
                        new_occ[i, j] = 1.0
                        break

        # Simple persistence metric
        if np.array_equal(new_occ, self.occupancy):
            self.shape_persistence += 1

        self.occupancy = new_occ

    # =================================================
    # SOUND FIELD
    # =================================================

    def _sense_sound(self, world):
        """
        Accumulates sound field from all rooms.
        """
        cx, cy, _ = self.center_xyz
        half = self.grid_size // 2

        field = np.zeros_like(self.sound)

        for place in world.places.values():
            if not hasattr(place, "rooms"):
                continue

            for room in place.rooms.values():
                if not hasattr(room, "get_sound_level"):
                    continue

                level = room.get_sound_level()
                if level <= 0:
                    continue

                bounds = getattr(room, "bounds", None)
                if not bounds:
                    continue

                (min_x, min_y, _), (max_x, max_y, _) = bounds
                rx = (min_x + max_x) / 2
                ry = (min_y + max_y) / 2

                for i in range(self.grid_size):
                    for j in range(self.grid_size):
                        wx = cx + (i - half) * self.resolution
                        wy = cy + (j - half) * self.resolution

                        d = math.hypot(wx - rx, wy - ry)
                        atten = 1.0 if d < 1 else 1.0 / max(d * d, 1.0)

                        field[i, j] += level * atten

        self.sound = np.clip(field, 0.0, 1.0)

    # =================================================
    # SNAPSHOT (ACCOUNTING)
    # =================================================

    def snapshot(self):
        return {
            "source": self.name,
            "type": "scout",
            "active": self.active,
            "frame": self.frame,
            "grid_size": self.grid_size,
            "resolution": self.resolution,
            "shape_persistence": int(self.shape_persistence),
            "occupancy_sum": int(self.occupancy.sum()),
            "sound_sum": float(round(self.sound.sum(), 3)),
        }