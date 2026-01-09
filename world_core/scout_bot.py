# world_core/scout_bot.py

import math
import numpy as np


class ScoutBot:
    """
    ScoutBot

    Focused, local observer.
    - No cognition
    - No naming
    - No decisions
    - Shape, depth, light, sound first

    Think:
    "Something was here, this far away, shaped like this,
     and it changed (or didn't)."
    """

    def __init__(
        self,
        name: str,
        origin_xyz,
        target_xyz,
        grid_size: int = 16,
        resolution: float = 1.0,
        max_frames: int = 30,
    ):
        self.name = name

        # -------------------------------------------------
        # Spatial anchors
        # -------------------------------------------------
        self.origin = np.array(origin_xyz, dtype=float)
        self.target = np.array(target_xyz, dtype=float)

        # -------------------------------------------------
        # Local Square (depth-aware)
        # -------------------------------------------------
        self.grid_size = grid_size
        self.resolution = resolution

        self.depth_grid = np.full((grid_size, grid_size), np.nan)
        self.occupancy_grid = np.zeros((grid_size, grid_size))
        self.light_grid = np.zeros((grid_size, grid_size))
        self.sound_grid = np.zeros((grid_size, grid_size))

        # -------------------------------------------------
        # Observation control
        # -------------------------------------------------
        self.frame = 0
        self.max_frames = max_frames
        self.active = True

        # -------------------------------------------------
        # Memory (raw sketches only)
        # -------------------------------------------------
        self.sketches = []

    # =================================================
    # PERCEPTION
    # =================================================

    def observe(self, world):
        """
        Observe the local environment.
        """
        if not self.active:
            return

        self.frame += 1
        self._clear_grids()

        # Observe places (static geometry)
        for place in world.places.values():
            self._project_point(
                place.position,
                light=0.2,
                sound=0.0,
            )

        # Observe agents (dynamic, sound-emitting)
        for agent in world.agents:
            if hasattr(agent, "position"):
                self._project_point(
                    agent.position,
                    light=0.0,
                    sound=getattr(agent, "emitted_sound_level", 0.0),
                )

        self._record_sketch()

        if self.frame >= self.max_frames:
            self.active = False

    # =================================================
    # PROJECTION (DEPTH + SHAPE)
    # =================================================

    def _project_point(self, xyz, light=0.0, sound=0.0):
        """
        Project a world point into the scout's local square.
        """
        rel = np.array(xyz, dtype=float) - self.origin
        dx, dy, dz = rel

        distance = math.sqrt(dx * dx + dy * dy + dz * dz)
        if distance <= 0:
            return

        half = self.grid_size // 2
        gx = int(half + dx / self.resolution)
        gy = int(half + dy / self.resolution)

        if 0 <= gx < self.grid_size and 0 <= gy < self.grid_size:
            self.depth_grid[gx, gy] = distance
            self.occupancy_grid[gx, gy] = 1
            self.light_grid[gx, gy] += light
            self.sound_grid[gx, gy] += sound

    # =================================================
    # MEMORY
    # =================================================

    def _record_sketch(self):
        """
        Store a raw perceptual sketch.
        """
        self.sketches.append({
            "frame": self.frame,
            "depth": np.nan_to_num(self.depth_grid).tolist(),
            "occupancy": self.occupancy_grid.tolist(),
            "light": self.light_grid.tolist(),
            "sound": self.sound_grid.tolist(),
        })

    def _clear_grids(self):
        self.depth_grid[:] = np.nan
        self.occupancy_grid[:] = 0
        self.light_grid[:] = 0
        self.sound_grid[:] = 0

    # =================================================
    # SHAPE PERSISTENCE (STEP 2)
    # =================================================

    def compute_shape_persistence(self):
        """
        Intersection-over-Union (IoU) of occupancy grids
        between last two frames.

        Measures:
        - Stability of outline
        - No interpretation
        """
        if len(self.sketches) < 2:
            return None

        prev = np.array(self.sketches[-2]["occupancy"])
        curr = np.array(self.sketches[-1]["occupancy"])

        intersection = np.sum((prev == 1) & (curr == 1))
        union = np.sum((prev == 1) | (curr == 1))

        if union == 0:
            return 0.0

        return intersection / union

    # =================================================
    # EXPORT → SALIENCE INVESTIGATOR
    # =================================================

    def export_report(self):
        """
        Export raw perception + persistence metrics.
        """
        return {
            "scout": self.name,
            "origin": self.origin.tolist(),
            "target": self.target.tolist(),
            "frames_observed": self.frame,
            "sketch_count": len(self.sketches),
            "shape_persistence": self.compute_shape_persistence(),
            "sketches": self.sketches,
        }

    # =================================================
    # SNAPSHOT (UI SAFE)
    # =================================================

    def snapshot(self):
        return {
            "agent": self.name,
            "type": "scout",
            "active": self.active,
            "frames": self.frame,
            "grid_size": self.grid_size,
            "resolution": self.resolution,
            "shape_persistence": self.compute_shape_persistence(),
        }