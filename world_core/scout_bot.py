# world_core/scout_bot.py

import numpy as np


class ScoutBot:
    """
    Scout Bot
    ----------
    Passive perceptual probe.
    Records local spatial fields (shape, sound, light).
    No cognition. No labels. No learning.
    """

    def __init__(
        self,
        name: str,
        grid_size: int = 16,
        resolution: float = 1.0,
        max_frames: int = 300,
    ):
        self.name = name
        self.grid_size = grid_size
        self.resolution = resolution
        self.max_frames = max_frames

        self.frame = 0
        self.active = True

        # Spatial fields
        self.occupancy = np.zeros((grid_size, grid_size))
        self.sound = np.zeros((grid_size, grid_size))
        self.light = np.zeros((grid_size, grid_size))

        # Persistence counters
        self.shape_persistence = 0
        self.last_occupancy = None

    # ==================================================
    # CORE OBSERVATION
    # ==================================================

    def observe(self, world):
        if not self.active:
            return

        self.frame += 1
        if self.frame > self.max_frames:
            self.active = False
            return

        # Reset fields
        self.occupancy[:] = 0
        self.sound[:] = 0
        self.light[:] = 0

        # ----------------------------------------------
        # 1️⃣ Capture geometry (SHAPE)
        # ----------------------------------------------
        for place in world.places.values():
            self._project_bounds(place)

            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    self._project_bounds(room)

                    # --------------------------------------
                    # 2️⃣ Capture EMISSIONS (LIGHT / SOUND)
                    # --------------------------------------
                    if hasattr(room, "objects"):
                        for obj in room.objects.values():
                            if hasattr(obj, "is_on") and obj.is_on:
                                self._emit_from_object(obj, room)

        # ----------------------------------------------
        # Persistence check
        # ----------------------------------------------
        if self.last_occupancy is not None:
            if np.array_equal(self.occupancy, self.last_occupancy):
                self.shape_persistence += 1
            else:
                self.shape_persistence = 0

        self.last_occupancy = self.occupancy.copy()

    # ==================================================
    # PROJECTION HELPERS
    # ==================================================

    def _project_bounds(self, entity):
        bounds = getattr(entity, "bounds", None)
        if not bounds:
            return

        (min_x, min_y, _), (max_x, max_y, _) = bounds

        for ix in range(self.grid_size):
            for iy in range(self.grid_size):
                wx = ix * self.resolution
                wy = iy * self.resolution

                if min_x <= wx <= max_x and min_y <= wy <= max_y:
                    self.occupancy[iy, ix] = 1

    def _emit_from_object(self, obj, room):
        """
        Emits light and sound into the grid when object is ON.
        """
        bounds = getattr(room, "bounds", None)
        if not bounds:
            return

        (min_x, min_y, _), (max_x, max_y, _) = bounds
        cx = (min_x + max_x) / 2
        cy = (min_y + max_y) / 2

        for ix in range(self.grid_size):
            for iy in range(self.grid_size):
                wx = ix * self.resolution
                wy = iy * self.resolution

                dx = wx - cx
                dy = wy - cy
                dist = max((dx * dx + dy * dy) ** 0.5, 1.0)

                # Inverse-square falloff
                intensity = min(1.0 / dist, 1.0)

                self.sound[iy, ix] += intensity
                self.light[iy, ix] += intensity

    # ==================================================
    # SNAPSHOT (FOR STREAMLIT / INVESTIGATOR)
    # ==================================================

    def snapshot(self):
        return {
            "source": "scout",
            "name": self.name,
            "type": "scout",
            "active": self.active,
            "frame": self.frame,
            "grid_size": self.grid_size,
            "resolution": self.resolution,
            "shape_persistence": self.shape_persistence,
            "occupancy_sum": int(self.occupancy.sum()),
            "sound_sum": round(float(self.sound.sum()), 3),
            "light_sum": round(float(self.light.sum()), 3),
        }