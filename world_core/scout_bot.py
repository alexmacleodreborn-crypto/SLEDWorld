# world_core/scout_bot.py

import math
import numpy as np


class ScoutBot:
    """
    Focused attention agent.

    Purpose:
    - Stake out a region of space
    - Record shape, distance, intensity (light/sound later)
    - NO interpretation
    - NO semantics
    """

    def __init__(
        self,
        name: str,
        anchor_xyz,
        grid_size: int = 16,
        resolution: float = 1.0,
        max_frames: int = 100,
    ):
        self.name = name
        self.anchor = tuple(anchor_xyz)

        self.grid_size = grid_size
        self.resolution = resolution
        self.max_frames = max_frames

        self.frames = 0
        self.active = True

        # Shape memory (occupancy)
        self.occupancy = np.zeros((grid_size, grid_size), dtype=int)
        self.last_occupancy = None
        self.shape_persistence = 0

    # ------------------------------------------------
    # OBSERVATION
    # ------------------------------------------------

    def observe(self, world):
        if not self.active:
            return

        self.frames += 1

        if self.frames >= self.max_frames:
            self.active = False
            return

        # Reset grid
        grid = np.zeros((self.grid_size, self.grid_size), dtype=int)

        ax, ay, az = self.anchor
        half = self.grid_size // 2

        for place in world.places.values():
            if not hasattr(place, "contains_world_point"):
                continue

            px, py, pz = place.position
            dx = (px - ax) / self.resolution
            dy = (py - ay) / self.resolution

            gx = int(round(dx)) + half
            gy = int(round(dy)) + half

            if 0 <= gx < self.grid_size and 0 <= gy < self.grid_size:
                grid[gy, gx] = 1

        # Shape persistence check
        if self.last_occupancy is not None:
            if np.array_equal(grid, self.last_occupancy):
                self.shape_persistence += 1
            else:
                self.shape_persistence = 0

        self.last_occupancy = grid.copy()
        self.occupancy = grid

    # ------------------------------------------------
    # SNAPSHOT
    # ------------------------------------------------

    def snapshot(self):
        return {
            "source": "scout",
            "name": self.name,
            "type": "scout",
            "active": self.active,
            "frames": self.frames,
            "grid_size": self.grid_size,
            "resolution": self.resolution,
            "shape_persistence": self.shape_persistence,
            "occupancy": self.occupancy.tolist(),
        }