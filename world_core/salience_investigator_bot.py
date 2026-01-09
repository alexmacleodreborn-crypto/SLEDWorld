import math
from collections import defaultdict


class SalienceInvestigatorBot:
    """
    Accounting / state-binding layer.

    Responsibilities:
    - Receive observer + scout snapshots
    - Track shape persistence signatures
    - Detect correlated intensity changes
    - Record STATE DELTAS (no semantics)
    """

    def __init__(self):
        self.frame = 0
        self.ledger = []

        # Shape memory
        self.shape_memory = {}  # shape_id -> last intensities
        self.shape_age = defaultdict(int)

        # Thresholds (deliberately simple)
        self.min_persistence = 3
        self.sound_delta_thresh = 0.15
        self.light_delta_thresh = 0.15

    # =================================================
    # INGESTION
    # =================================================

    def ingest_scout_snapshot(self, scout_snapshot: dict):
        """
        Scout snapshot must include:
        - shape_signature
        - sound_level
        - light_level
        - persistence
        """

        self.frame += 1

        shape_id = scout_snapshot.get("shape_signature")
        persistence = scout_snapshot.get("shape_persistence", 0)

        sound = scout_snapshot.get("sound_level", 0.0)
        light = scout_snapshot.get("light_level", 0.0)

        if shape_id is None:
            return

        self.shape_age[shape_id] += 1

        # Only consider stable shapes
        if persistence < self.min_persistence:
            self.shape_memory[shape_id] = (sound, light)
            return

        prev = self.shape_memory.get(shape_id)

        if prev is not None:
            prev_sound, prev_light = prev

            sound_delta = sound - prev_sound
            light_delta = light - prev_light

            # Correlated intensity change
            if (
                abs(sound_delta) >= self.sound_delta_thresh
                or abs(light_delta) >= self.light_delta_thresh
            ):
                self._record_state_change(
                    shape_id=shape_id,
                    sound_delta=sound_delta,
                    light_delta=light_delta,
                    persistence=persistence,
                )

        self.shape_memory[shape_id] = (sound, light)

    # =================================================
    # STATE RECORD
    # =================================================

    def _record_state_change(
        self,
        shape_id: str,
        sound_delta: float,
        light_delta: float,
        persistence: int,
    ):
        entry = {
            "frame": self.frame,
            "shape_id": shape_id,
            "state_delta": {
                "sound": round(sound_delta, 3),
                "light": round(light_delta, 3),
            },
            "direction": (
                "up"
                if (sound_delta + light_delta) > 0
                else "down"
            ),
            "persistence": persistence,
        }

        self.ledger.append(entry)

    # =================================================
    # SNAPSHOT
    # =================================================

    def snapshot(self):
        return {
            "frames_processed": self.frame,
            "known_shapes": len(self.shape_memory),
            "state_events": len(self.ledger),
        }