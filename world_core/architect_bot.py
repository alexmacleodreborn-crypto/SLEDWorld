# world_core/architect_bot.py

class ArchitectBot:
    """
    Pattern recogniser.
    Reads geometry + repetition from ledger.
    Proposes structural symbols (brick, wall, room).
    """

    def __init__(self):
        self.name = "Architect"
        self.known_patterns = set()
        self.proposals = []

        # thresholds
        self.min_surface_repeats = 12
        self.min_wall_planes = 4

    def review(self, ledger):
        if not ledger.events:
            return

        # --- Detect BRICK-like repetition ---
        surface_hits = 0
        for e in ledger.events[-300:]:
            if e.get("source") == "surveyor":
                surf = e.get("surface_volume")
                if surf:
                    surface_hits += 1

        if surface_hits >= self.min_surface_repeats:
            self._propose("BRICK_PATTERN", surface_hits)

        # --- Detect WALL planes ---
        wall_votes = 0
        for e in ledger.events[-300:]:
            if e.get("source") == "surveyor":
                shape = e.get("volume_shape")
                if shape and shape[2] > 4:
                    wall_votes += 1

        if wall_votes >= self.min_wall_planes:
            self._propose("WALL_STRUCTURE", wall_votes)

    def _propose(self, symbol, evidence):
        if symbol in self.known_patterns:
            return

        proposal = {
            "source": "architect",
            "symbol": symbol,
            "evidence": evidence,
            "status": "proposed",
        }
        self.known_patterns.add(symbol)
        self.proposals.append(proposal)

    def snapshot(self):
        return {
            "source": "architect",
            "known_patterns": list(self.known_patterns),
            "proposals": self.proposals[-10:],
        }