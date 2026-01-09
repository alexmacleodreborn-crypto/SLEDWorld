# world_core/salience_investigator_bot.py

class SalienceInvestigatorBot:
    """
    Accounting / memory layer.
    Does not perceive directly.
    Receives structured reports from other agents.
    """

    def __init__(self):
        # Frame counter = how many world frames processed
        self.frame_counter = 0

        # Ledger of all ingested reports
        self.ledger = []

        # Simple tallies (expand later)
        self.sources_seen = {}
        self.event_counts = {}

    # =================================================
    # INGESTION
    # =================================================

    def ingest(self, snapshot: dict):
        """
        Accepts a snapshot from any agent.
        Snapshot MUST contain 'source'.
        """

        if not isinstance(snapshot, dict):
            return

        source = snapshot.get("source", "unknown")

        # Frame advances when ANY snapshot is ingested
        self.frame_counter += 1

        # Track sources
        self.sources_seen[source] = self.sources_seen.get(source, 0) + 1

        # Track events if present
        event = snapshot.get("event")
        if event:
            self.event_counts[event] = self.event_counts.get(event, 0) + 1

        # Store full snapshot (append-only memory)
        self.ledger.append(snapshot)

    # =================================================
    # OBSERVER VIEW
    # =================================================

    def snapshot(self):
        return {
            "type": "salience_investigator",
            "frames_processed": self.frame_counter,
            "total_transactions": len(self.ledger),
            "sources_seen": self.sources_seen,
            "event_counts": self.event_counts,
        }