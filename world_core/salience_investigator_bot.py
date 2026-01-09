# world_core/salience_investigator_bot.py

from world_core.scout_bot import ScoutBot


class SalienceInvestigatorBot:
    """
    Accounting + attention allocator.
    """

    def __init__(self):
        self.frame = 0
        self.ledger = []

        # Simple salience counters
        self.sound_events = 0

    # -------------------------
    # INGESTION
    # -------------------------

    def ingest_physical_event(self, event):
        self.ledger.append({
            "source": "walker",
            "frame": self.frame,
            "event": event,
        })

        if event.get("sound_emitted", 0) > 0:
            self.sound_events += 1

    def ingest_observer_snapshot(self, snapshot):
        self.frame += 1
        self.ledger.append({
            "source": "observer",
            "frame": self.frame,
            "snapshot": snapshot,
        })

    def ingest_scout_report(self, report):
        self.ledger.append({
            "source": "scout",
            "frame": self.frame,
            "report": report,
        })

    # -------------------------
    # ATTENTION ALLOCATION
    # -------------------------

    def spawn_scouts_if_needed(self):
        """
        If repeated sound events occur, allocate a scout.
        """
        scouts = []

        if self.sound_events >= 2:
            # Reset counter to avoid infinite spawning
            self.sound_events = 0

            scout = ScoutBot(
                name=f"Scout-sound-{self.frame}",
                origin_xyz=(4800, 5100, 0),
                target_xyz=(4800, 5100, 0),
                grid_size=16,
                resolution=1.0,
                max_frames=20,
            )
            scouts.append(scout)

        return scouts

    # -------------------------
    # SNAPSHOT (UI)
    # -------------------------

    def snapshot(self):
        return {
            "frames_processed": self.frame,
            "ledger_entries": len(self.ledger),
        }