# world_core/builder_bot.py

class BuilderBot:
    """
    Structure assembler.
    Reads Architect + Manager approvals.
    Confirms higher-order structures.
    """

    def __init__(self):
        self.name = "Builder"
        self.built = set()
        self.events = []

    def review(self, ledger):
        approvals = []
        for e in ledger.events:
            if e.get("symbol") and e.get("note", "").startswith("Approved"):
                approvals.append(e["symbol"])

        # --- Build WALL ---
        if "BRICK_PATTERN" in approvals and "WALL" not in self.built:
            self._build("WALL")

        # --- Build ROOM ---
        if "WALL_STRUCTURE" in approvals and "ROOM" not in self.built:
            self._build("ROOM")

    def _build(self, structure):
        self.built.add(structure)
        self.events.append({
            "source": "builder",
            "structure": structure,
            "status": "confirmed",
        })

    def snapshot(self):
        return {
            "source": "builder",
            "built_structures": list(self.built),
            "events": self.events[-10:],
        }