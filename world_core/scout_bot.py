# world_core/scout_bot.py

import math
import uuid
from collections import defaultdict


class ScoutBot:
    """
    Scout Bot — Pre-concept Perception Agent

    Purpose:
    - Stake out a region
    - Perceive shape, distance, and intensity
    - Report salience WITHOUT object labels

    Philosophy:
    - No time semantics (time is a coordinate)
    - No language
    - No objects
    - Shape precedes meaning
    """

    def __init__(
        self,
        name: str,
        anchor_xyz,
        radius: float = 25.0,
        grid_size: int = 16,
        resolution: float = 1.0,
    ):
        self.id = f"scout-{uuid.uuid4().hex[:6]}"
        self.name = name
        self.anchor = anchor_xyz
        self.radius = radius

        # Square-like perception
        self.grid_size = grid_size
        self.resolution = resolution

        # Internal counters
        self.frames = 0
        self.shape_persistence = 0

        # Last perceived square (for persistence)
        self._last_occupancy = None

        # Ledger (local, before investigator)
        self.local_log = []

        self.active = True

    # ==================================================
    # PERCEPTION ENTRY POINT
    # ==================================================

    def observe(self, world):
        """
        Called once per world tick.
        """
        if not self.active:
            return

        self.frames += 1

        occupancy = self._scan_occupancy(world)
        sound_level = self._scan_sound(world)
        light_level = self._scan_light(world)

        persistence = self._compute_persistence(occupancy)

        report = {
            "type": "scout",
            "scout_id": self.id,
            "name": self.name,
            "frame": self.frames,
            "anchor": self.anchor,
            "grid_size": self.grid_size,
            "resolution": self.resolution,
            "distance_radius": self.radius,
            "occupancy": occupancy,
            "sound": sound_level,
            "light": light_level,
            "shape_persistence": persistence,
        }

        self.local_log.append(report)

        # Forward to accounting layer if present
        if hasattr(world, "salience_investigator"):
            world.salience_investigator.ingest_scout_report(report)

    # ==================================================
    # OCCUPANCY / SHAPE
    # ==================================================

    def _scan_occupancy(self, world):
        """
        Produces a grid of occupancy values:
        0 = empty
        1 = something present
        """
        half = self.grid_size // 2
        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        ax, ay, az = self.anchor

        for place in world.places.values():
            if not hasattr(place, "contains_world_point"):
                continue

            for ix in range(self.grid_size):
                for iy in range(self.grid_size):
                    dx = (ix - half) * self.resolution
                    dy = (iy - half) * self.resolution

                    px = ax + dx
                    py = ay + dy
                    pz = az

                    if place.contains_world_point((px, py, pz)):
                        grid[iy][ix] = 1

        return grid

    # ==================================================
    # SOUND (INTENSITY FIELD)
    # ==================================================

    def _scan_sound(self, world):
        total = 0.0
        ax, ay, az = self.anchor

        for place in world.places.values():
            if not hasattr(place, "rooms"):
                continue

            for room in place.rooms.values():
                if not hasattr(room, "get_sound_level"):
                    continue

                source = room.get_sound_level()
                if source <= 0:
                    continue

                cx, cy, cz = room.center_xyz()
                d = math.dist((ax, ay, az), (cx, cy, cz))

                if d <= self.radius:
                    attenuation = max(1.0 / (d * d + 1.0), 0.02)
                    total += source * attenuation

        return round(min(total, 1.0), 3)

    # ==================================================
    # LIGHT (PLACEHOLDER FIELD)
    # ==================================================

    def _scan_light(self, world):
        """
        Placeholder for future light field.
        For now: presence density proxy.
        """
        occupancy = self._last_occupancy or []
        if not occupancy:
            return 0.0

        filled = sum(sum(row) for row in occupancy)
        total = self.grid_size * self.grid_size

        return round(filled / total, 3)

    # ==================================================
    # SHAPE PERSISTENCE
    # ==================================================

    def _compute_persistence(self, occupancy):
        """
        Detects whether shape is stable across frames.
        """
        if self._last_occupancy is None:
            self._last_occupancy = occupancy
            self.shape_persistence = 0
            return 0

        same = 0
        total = self.grid_size * self.grid_size

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if occupancy[y][x] == self._last_occupancy[y][x]:
                    same += 1

        similarity = same / total

        if similarity > 0.9:
            self.shape_persistence += 1
        else:
            self.shape_persistence = 0

        self._last_occupancy = occupancy
        return self.shape_persistence

    # ==================================================
    # OBSERVER VIEW
    # ==================================================

    def snapshot(self):
        return {
            "id": self.id,
            "type": "scout",
            "active": self.active,
            "frames": self.frames,
            "grid_size": self.grid_size,
            "resolution": self.resolution,
            "shape_persistence": self.shape_persistence,
        }