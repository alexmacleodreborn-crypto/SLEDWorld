# world_core/architect_bot.py

class ArchitectBot:
    """
    Reads schematics/ledger and groups repeating surface motifs into structures.
    Stage-0: heuristic pattern grouping only.
    """

    def __init__(self, name="Architect-1"):
        self.name = name
        self.last_snapshot = {"source": "architect", "name": self.name, "structures": []}

    def observe(self, world):
        ledger = getattr(world, "salience_investigator", None)
        entries = getattr(ledger, "ledger", []) if ledger else []

        # Placeholder: detect repeated 'surveyor' or 'shape' mentions
        shape_events = [e for e in entries if isinstance(e, dict) and (e.get("focus") == "shape" or e.get("source") == "surveyor")]

        self.last_snapshot = {
            "source": "architect",
            "name": self.name,
            "frame": getattr(world, "frame", None),
            "shape_events_seen": len(shape_events),
            "structures": [
                {"label": "candidate_wall", "confidence": 0.3 + min(len(shape_events) / 1000.0, 0.6)}
            ] if shape_events else []
        }

    def snapshot(self):
        return self.last_snapshot