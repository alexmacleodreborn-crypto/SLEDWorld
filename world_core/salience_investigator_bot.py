class SalienceInvestigatorBot:
    """
    Integrates observer reports into certainty fields.
    This is where structure becomes real.
    """

    def __init__(self):
        self.frame_counter = 0

        # Raw history
        self.ledger = []

        # Accumulated certainty
        self.room_certainty = {}

    # =================================================
    # INGEST RAW REPORT
    # =================================================

    def ingest(self, snapshot: dict):
        self.frame_counter += 1
        self.ledger.append(snapshot)

        for room in snapshot.get("rooms", []):
            name = room["room"]

            if name not in self.room_certainty:
                self.room_certainty[name] = {
                    "sound_sum": 0.0,
                    "light_sum": 0.0,
                    "frames_seen": 0,
                }

            entry = self.room_certainty[name]
            entry["sound_sum"] += room.get("sound_level", 0.0)
            entry["light_sum"] += room.get("light_level", 0.0)
            entry["frames_seen"] += 1

    # =================================================
    # DERIVED CERTAINTY (THIS IS WHAT SCOUT USES)
    # =================================================

    def get_room_signatures(self):
        signatures = {}

        for room, data in self.room_certainty.items():
            frames = max(data["frames_seen"], 1)

            signatures[room] = {
                "sound_signature": round(data["sound_sum"] / frames, 3),
                "light_signature": round(data["light_sum"] / frames, 3),
                "certainty": frames,
            }

        return signatures

    # =================================================
    # SNAPSHOT (FOR STREAMLIT)
    # =================================================

    def snapshot(self):
        return {
            "frames_processed": self.frame_counter,
            "rooms": self.get_room_signatures(),
        }