# world_core/salience_investigator_bot.py

from collections import defaultdict
from typing import Dict, Any, List


class SalienceInvestigatorBot:
    """
    Sandy’s Law Ledger.

    This is the ONLY authority for:
    - pattern stability
    - structural confidence
    - semantic readiness

    All bots REPORT.
    This bot DECIDES.
    """

    def __init__(self):
        # Raw ledger
        self.ledger: List[Dict[str, Any]] = []

        # Counters
        self.total_events = 0
        self.pattern_hits = 0
        self.confirmed_structures = 0

        # Symbol memory
        self.symbol_occurrences = defaultdict(int)
        self.stable_symbols = set()

        # Frame tracking
        self.frame_counter = 0

    # ==================================================
    # INGESTION
    # ==================================================

    def ingest(self, snapshot: Dict[str, Any], world=None):
        """
        Ingests a snapshot from ANY bot.
        Snapshot MUST include:
        - source
        - frame
        """

        self.total_events += 1
        self.frame_counter = max(self.frame_counter, snapshot.get("frame", 0))
        self.ledger.append(snapshot)

        source = snapshot.get("source", "unknown")

        # --------------------------
        # Pattern detection
        # --------------------------
        if source in {"observer", "scout", "surveyor"}:
            self.pattern_hits += 1

        # --------------------------
        # Structural confirmation
        # --------------------------
        if source == "surveyor":
            if snapshot.get("surface_volume"):
                self.confirmed_structures += 1

        # --------------------------
        # Symbol tracking
        # --------------------------
        symbol = snapshot.get("symbol")
        if symbol:
            self.symbol_occurrences[symbol] += 1

            # Symbol becomes stable only after repetition
            if self.symbol_occurrences[symbol] >= 3:
                self.stable_symbols.add(symbol)

    # ==================================================
    # SANDY’S LAW GATES
    # ==================================================

    def pattern_stability_score(self) -> float:
        """
        Z gate — repetition suppresses chaos.
        """
        if self.total_events == 0:
            return 0.0

        return round(self.pattern_hits / self.total_events, 3)

    def structure_confidence_score(self) -> float:
        """
        Σ → structure collapse gate.
        """
        if self.pattern_hits == 0:
            return 0.0

        return round(self.confirmed_structures / self.pattern_hits, 3)

    def semantic_readiness_score(self) -> float:
        """
        Symbol → word ignition gate.
        """
        if self.confirmed_structures == 0:
            return 0.0

        return round(len(self.stable_symbols) / self.confirmed_structures, 3)

    # ==================================================
    # MANAGER DECISION
    # ==================================================

    def manager_approval(self) -> Dict[str, bool]:
        """
        Final arbitration layer.
        """

        return {
            "patterns_stable": self.pattern_stability_score() >= 0.6,
            "structure_confirmed": self.structure_confidence_score() >= 0.5,
            "language_ready": self.semantic_readiness_score() >= 0.3,
        }

    # ==================================================
    # SNAPSHOT
    # ==================================================

    def snapshot(self) -> Dict[str, Any]:
        return {
            "frame": self.frame_counter,
            "events": self.total_events,
            "patterns": self.pattern_hits,
            "structures": self.confirmed_structures,
            "stable_symbols": list(self.stable_symbols),
            "pattern_stability": self.pattern_stability_score(),
            "structure_confidence": self.structure_confidence_score(),
            "semantic_readiness": self.semantic_readiness_score(),
            "manager_approval": self.manager_approval(),
        }