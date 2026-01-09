class SalienceInvestigatorBot:
    """
    Accounting / state-binding layer.
    Single ingestion interface.
    """

    def __init__(self):
        self.frame = 0
        self.ledger = []

        self.shape_memory = {}
        self.min_persistence = 3
        self.sound_delta_thresh = 0.15
        self.light_delta_thresh = 0.15

    # =================================================
    # SINGLE INGESTION CONTRACT
    # =================================================

    def ingest(self, snapshot: dict):
        """
        Accepts any snapshot with a declared 'source'.
        """
        self.frame += 1

        source = snapshot.get("source")

        if source == "scout":
            self._handle_scout(snapshot)

        # Observer, walker, others can be added later
        # without breaking anything

    # =================================================
    # SCOUT HANDLING (STEP 1 & 2)
    # =================================================

    def _handle_scout(self, snap):
        shape_id = snap.get("shape_signature")
        persistence = snap.get("shape_persistence", 0)

        sound = snap.get("sound_level", 0.0)
        light = snap.get("light_level", 0.0)

        if shape_id is None:
            return

        prev = self.shape_memory.get(shape_id)

        if prev and persistence >= self.min_persistence:
            prev_sound, prev_light = prev

            if (
                abs(sound - prev_sound) >= self.sound_delta_thresh
                or abs(light - prev_light) >= self.light_delta_thresh
            ):
                self.ledger.append({
                    "frame": self.frame,
                    "shape_id": shape_id,
                    "state_delta": {
                        "sound": round(sound - prev_sound, 3),
                        "light": round(light - prev_light, 3),
                    },
                    "direction": "up" if (sound + light) > (prev_sound + prev_light) else "down",
                    "persistence": persistence,
                })

        self.shape_memory[shape_id] = (sound, light)

    # =================================================
    # SNAPSHOT
    # =================================================

    def snapshot(self):
        return {
            "frames_processed": self.frame,
            "known_shapes": len(self.shape_memory),
            "state_events": len(self.ledger),
        }