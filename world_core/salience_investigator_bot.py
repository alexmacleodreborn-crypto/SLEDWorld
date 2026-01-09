# world_core/salience_investigator_bot.py

class SalienceInvestigatorBot:
    """
    Accounting layer.
    No cognition. No action.
    Builds structured memory.
    """

    def __init__(self):
        self.frame_counter = 0
        self.ledger = []
        self.patterns = {}

    # -------------------------------------------------
    # INGEST FROM OBSERVER
    # -------------------------------------------------
    def ingest_observer_snapshot(self, snapshot):
        self.frame_counter += 1

        entry = {
            "frame": self.frame_counter,
            "source": "observer",
            "data": snapshot,
        }
        self.ledger.append(entry)

        self._accumulate_patterns(snapshot)

    # -------------------------------------------------
    # INGEST FROM WALKER
    # -------------------------------------------------
    def ingest_physical_event(self, event):
        entry = {
            "frame": self.frame_counter,
            "source": "walker",
            "data": event,
        }
        self.ledger.append(entry)

        if event.get("sound_emitted", 0) > 0:
            self.patterns["sound_emission"] = (
                self.patterns.get("sound_emission", 0) + 1
            )

    # -------------------------------------------------
    # PATTERN ACCUMULATION (NO INTERPRETATION)
    # -------------------------------------------------
    def _accumulate_patterns(self, snapshot):
        if snapshot.get("heard_sound_events", 0) > 0:
            self.patterns["heard_sound"] = (
                self.patterns.get("heard_sound", 0) + 1
            )

    # -------------------------------------------------
    # SNAPSHOT (UI)
    # -------------------------------------------------
    def snapshot(self):
        return {
            "frames_processed": self.frame_counter,
            "total_records": len(self.ledger),
            "patterns": dict(self.patterns),
        }