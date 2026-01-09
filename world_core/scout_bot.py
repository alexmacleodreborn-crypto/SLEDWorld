# world_core/scout_bot.py

import numpy as np


class ScoutBot:
    """
    Scout: stakeout for N frames.
    Builds a local grid around a target room (or around walker area if not provided).

    Outputs:
      - occupancy grid (shape)
      - sound grid
      - light grid
      - persistence score (shape)
    """

    def __init__(
        self,
        name: str,
        target_room_name: str | None = None,
        grid_size: int = 32,
        resolution: float = 1.0,  # meters per cell (conceptual)
        max_frames: int = 200,
    ):
        self.name = name
        self.target_room_name = target_room_name

        self.grid_size = int(grid_size)
        self.resolution = float(resolution)
        self.max_frames = int(max_frames)

        self.active = True
        self.frames = 0

        self.last_occupancy_hash = None
        self.shape_persistence = 0

        self.occupancy = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        self.sound = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        self.light = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)

        self.last_signals = {"sound": 0.0, "light_intensity": 0.0, "light_color": "none"}
        self.ledger = []

        self._current_area = "world"

    def _hash_grid(self, g: np.ndarray) -> int:
        # Cheap stable hash
        return int(np.sum(g * 1000) + np.sum(g.shape))

    def _resolve_room_snapshot(self, world):
        # Find the target room snapshot
        places = getattr(world, "places", {}) or {}
        for place in places.values():
            rooms = getattr(place, "rooms", None)
            if not rooms:
                continue
            for room in rooms.values():
                if self.target_room_name and getattr(room, "name", None) != self.target_room_name:
                    continue
                try:
                    return room, room.snapshot()
                except Exception:
                    return room, {}
        return None, {}

    def observe(self, world):
        if not self.active:
            return

        self.frames += 1
        if self.frames >= self.max_frames:
            self.active = False

        room, rs = self._resolve_room_snapshot(world)
        if room is None:
            # no room yet; blank grids
            self.occupancy[:] = 0
            self.sound[:] = 0
            self.light[:] = 0
            self._current_area = "world"
            return

        self._current_area = getattr(room, "name", "room")

        # --- Occupancy: very simple "objects exist" marking
        occ = np.zeros_like(self.occupancy)

        objs = rs.get("objects", {}) or {}
        # Put dots for each object to create "shape signature"
        # (Cheap starter: maps each object to a deterministic cell)
        i = 0
        for oname, osnap in objs.items():
            cx = (i * 7 + 3) % self.grid_size
            cy = (i * 11 + 5) % self.grid_size
            occ[cy, cx] = 1.0
            i += 1

        self.occupancy = occ

        # --- Signals
        sig = rs.get("signals", {}) or {}
        sound_lvl = float(sig.get("sound", 0.0) or 0.0)
        light_sig = sig.get("light") or {"intensity": 0.0, "color": "none"}
        light_int = float(light_sig.get("intensity", 0.0) or 0.0)
        light_color = str(light_sig.get("color", "none"))

        # Build uniform fields (starter)
        self.sound[:] = sound_lvl
        self.light[:] = light_int

        # --- Persistence: does shape stay the same?
        h = self._hash_grid(self.occupancy)
        if self.last_occupancy_hash is None:
            self.last_occupancy_hash = h
        else:
            if h == self.last_occupancy_hash:
                self.shape_persistence += 1
            else:
                self.shape_persistence = 0
                self.last_occupancy_hash = h

        self.last_signals = {
            "sound": round(sound_lvl, 3),
            "light_intensity": round(light_int, 3),
            "light_color": light_color,
        }

        self.ledger.append({
            "frame": self.frames,
            "area": self._current_area,
            "sound": round(sound_lvl, 3),
            "light": {"intensity": round(light_int, 3), "color": light_color},
            "shape_persistence": self.shape_persistence,
        })

    def snapshot(self):
        return {
            "source": "scout",
            "type": "scout",
            "name": self.name,
            "frame": self.frames,
            "active": self.active,
            "grid_size": self.grid_size,
            "resolution": self.resolution,
            "area": self._current_area,
            "shape_persistence": self.shape_persistence,
            "signals": {
                "sound": self.last_signals["sound"],
                "light": {
                    "intensity": self.last_signals["light_intensity"],
                    "color": self.last_signals["light_color"],
                },
            },
            "ledger_tail": self.ledger[-10:],
        }