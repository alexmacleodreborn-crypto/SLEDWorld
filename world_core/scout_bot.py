# world_core/scout_bot.py

import numpy as np


class ScoutBot:
    """
    Shape-first perception agent.

    Learns:
    - distance
    - outline
    - persistence

    Does NOT learn:
    - names
    - meaning
    """

    def __init__(
        self,
        name: str,
        anchor_xyz,
        grid_size: int = 16,
        resolution: float = 1.0,
        max_frames: int = 200,
    ):
        self.name = name
        self.anchor = tuple(anchor_xyz)

        self.grid_size = grid_size
        self.resolution = resolution
        self.max_frames = max_frames

        self.frames = 0
        self.active = True

        self.occupancy = np.zeros((grid_size, grid_size), dtype=int)
        self.last_occupancy = None
        self.shape_persistence = 0

    # ------------------------------------------------
    # OBSERVE SPACE
    # ------------------------------------------------

    def observe(self, world):
        if not self.active:
            return

        self.frames += 1
        if self.frames >= self.max_frames:
            self.active = False
            return

        grid = np.zeros((self.grid_size, self.grid_size), dtype=int)

        ax, ay, az = self.anchor
        half = self.grid_size // 2

        # 🔹 Scan ALL spatial bounds (rooms + places)
        for place in world.places.values():

            # --- Rooms (preferred: real geometry)
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if not hasattr(room, "bounds"):
                        continue

                    (min_x, min_y, _), (max_x, max_y, _) = room.bounds

                    self._rasterise_bounds(
                        min_x, min_y,
                        max_x, max_y,
                        ax, ay,
                        grid, half
                    )

            # --- Fallback: place bounds
            if hasattr(place, "bounds") and place.bounds:
                (min_x, min_y, _), (max_x, max_y, _) = place.bounds

                self._rasterise_bounds(
                    min_x, min_y,
                    max_x, max_y,
                    ax, ay,
                    grid, half
                )

        # -------------------------------
        # Shape persistence
        # -------------------------------
        if self.last_occupancy is not None:
            if np.array_equal(grid, self.last_occupancy):
                self.shape_persistence += 1
            else:
                self.shape_persistence = 0

        self.last_occupancy = grid.copy()
        self.occupancy = grid

    # ------------------------------------------------
    # DRAW OUTLINE INTO GRID
    # ------------------------------------------------

    def _rasterise_bounds(
        self,
        min_x, min_y,
        max_x, max_y,
        ax, ay,
        grid, half
    ):
        step = self.resolution

        x = min_x
        while x <= max_x:
            self._plot(x, min_y, ax, ay, grid, half)
            self._plot(x, max_y, ax, ay, grid, half)
            x += step

        y = min_y
        while y <= max_y:
            self._plot(min_x, y, ax, ay, grid, half)
            self._plot(max_x, y, ax, ay, grid, half)
            y += step

    def _plot(self, wx, wy, ax, ay, grid, half):
        gx = int(round((wx - ax) / self.resolution)) + half
        gy = int(round((wy - ay) / self.resolution)) + half

        if 0 <= gx < self.grid_size and 0 <= gy < self.grid_size:
            grid[gy, gx] = 1

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