# world_core/scout_bot.py

import numpy as np


class ScoutBot:
    """
    Scout Bot (Ledger-Driven)

    Purpose:
    - Sample CERTAINTY, not raw sensation
    - Visualise confirmed structure (shape)
    - Visualise confirmed energy signatures (sound, light)

    Rules:
    - NEVER reads world objects directly
    - NEVER reads observer directly
    - ONLY reads Salience Investigator outputs
    - No cognition
    - No learning
    """

    def __init__(
        self,
        name: str,
        grid_size: int = 16,
        resolution: float = 1.0,
        max_frames: int = 500,
        certainty_threshold: int = 5,
    ):
        self.name = name
        self.type = "scout"

        self.grid_size = grid_size
        self.resolution = resolution
        self.max_frames = max_frames
        self.certainty_threshold = certainty_threshold

        self.frame = 0
        self.active = False  # ACTIVATED BY SALIENCE ONLY

        # Ledger-derived fields
        self.shape = np.zeros((grid_size, grid_size))
        self.sound = np.zeros((grid_size, grid_size))
        self.light = np.zeros((grid_size, grid_size))

        # Diagnostics
        self.rooms_seen = {}
        self.confirmed_rooms = set()

    # =================================================
    # OBSERVATION (CERTAINTY ONLY)
    # =================================================

    def observe(self, world):
        """
        Scout samples ONLY confirmed ledger signatures.
        """

        investigator = getattr(world, "salience_investigator", None)
        if investigator is None:
            return

        signatures = investigator.get_room_signatures()
        if not signatures:
            return

        self.active = True
        self.frame += 1

        # Reset grids slowly (persistence)
        self.shape *= 0.95
        self.sound *= 0.90
        self.light *= 0.90

        for room_name, sig in signatures.items():
            certainty = sig.get("certainty", 0)

            # -----------------------------------------
            # Track persistence
            # -----------------------------------------
            self.rooms_seen[room_name] = certainty

            if certainty < self.certainty_threshold:
                continue

            # -----------------------------------------
            # CONFIRMED STRUCTURE
            # -----------------------------------------
            self.confirmed_rooms.add(room_name)

            # Deterministic projection (room → grid cell)
            gx = hash(room_name) % self.grid_size
            gy = (hash(room_name) // self.grid_size) % self.grid_size

            # Shape = confirmed existence
            self.shape[gy, gx] = min(1.0, self.shape[gy, gx] + 0.3)

            # Sound signature
            sound_sig = sig.get("sound_signature", 0.0)
            if sound_sig > 0:
                self.sound[gy, gx] = min(
                    1.0, self.sound[gy, gx] + sound_sig
                )

            # Light signature
            light_sig = sig.get("light_signature", 0.0)
            if light_sig > 0:
                self.light[gy, gx] = min(
                    1.0, self.light[gy, gx] + light_sig
                )

        if self.frame >= self.max_frames:
            self.active = False

    # =================================================
    # SNAPSHOT (FOR STREAMLIT / DEBUG)
    # =================================================

    def snapshot(self):
        return {
            "source": self.name,
            "type": "scout",
            "active": self.active,
            "frame": self.frame,
            "grid_size": self.grid_size,
            "certainty_threshold": self.certainty_threshold,
            "rooms_seen": self.rooms_seen,
            "confirmed_rooms": list(self.confirmed_rooms),
            "shape_energy": round(float(self.shape.sum()), 3),
            "sound_energy": round(float(self.sound.sum()), 3),
            "light_energy": round(float(self.light.sum()), 3),
        }