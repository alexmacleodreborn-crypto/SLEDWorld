# world_core/salience_investigator_bot.py

class SalienceInvestigatorBot:
    """
    Central transaction ledger.
    This is NOT a thinker.
    It only records, tags, and gates information.
    """

    def __init__(self):
        self.name = "Ledger"
        self.events = []
        self.frame_counter = 0

    # -------------------------------------------------
    # INGEST (single gate for Sandy’s Law)
    # -------------------------------------------------

    def ingest(self, event: dict, world=None):
        """
        Record an event if valid.
        """
        if not isinstance(event, dict):
            return

        self.frame_counter += 1

        record = dict(event)
        record["_frame"] = self.frame_counter

        # Optional world context (safe)
        if world is not None:
            record["_world_frame"] = getattr(world, "frame", None)

        self.events.append(record)

    # -------------------------------------------------
    # Snapshot for Streamlit
    # -------------------------------------------------

    def snapshot(self):
        return {
            "source": "ledger",
            "frames": self.frame_counter,
            "events_recorded": len(self.events),
            "recent_events": self.events[-10:],
        }