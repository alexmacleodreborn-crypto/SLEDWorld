# world_core/scout_bot.py

import numpy as np

class ScoutBot:
    """
    Scout bot.
    Passive local field sampler.
    No cognition, no learning.
    """

    def __init__(
        self,
        name: str,
        grid_size: int = 16,
        resolution: int = 1,
        max_frames: int = 300,
    ):
        self.name = name
        self.type = "scout"

        self.grid_size = grid_size
        self.resolution = resolution
        self.max_frames = max_frames

        self.frame = 0
        self.active = True

        # Perception fields
        self.occupancy = np.zeros((grid_size, grid_size))
        self.sound = np.zeros((grid_size, grid_size))
        self.light = np.zeros((grid_size, grid_size))

        self.shape_persistence = 0

    # -----------------------------------------
    # OBSERVATION
    # -----------------------------------------

    def observe(self, world):
        """
        Sample world fields.
        Currently placeholder → structure exists.
        """

        if not self.active:
            return

        self.frame += 1

        # --- placeholder sampling ---
        # These will later be driven by sound/light fields
        self.sound *= 0.95
        self.light *= 0.95

        if self.frame >= self.max_frames:
            self.active = False

    # -----------------------------------------
    # SNAPSHOT
    # -----------------------------------------

    def snapshot(self):
        return {
            "source": self.name,
            "type": "scout",
            "active": self.active,
            "frame": self.frame,
            "grid_size": self.grid_size,
            "resolution": self.resolution,
            "shape_persistence": self.shape_persistence,
        }