# world_core/ledger.py

from dataclasses import dataclass, field
from typing import List, Dict, Any

from world_core.sandys_square import coherence_gate


# ============================================================
# Ledger Event
# ============================================================

@dataclass
class LedgerEvent:
    """
    Atomic record of a world observation or inference.
    """
    frame: int
    source: str
    payload: Dict[str, Any]


# ============================================================
# Ledger Core
# ============================================================

@dataclass
class Ledger:
    """
    Central truth table of the world.
    """

    events: List[LedgerEvent] = field(default_factory=list)

    # Rolling metrics
    pattern_stability: float = 0.0
    square_coherence: Dict[str, Any] = field(default_factory=dict)
    semantic_readiness: float = 0.0

    # Internal buffers
    _recent_points: List[Dict[str, Any]] = field(default_factory=list)

    # ========================================================
    # Ingest
    # ========================================================

    def ingest(self, event: LedgerEvent):
        self.events.append(event)

        self._recent_points.append({
            "source": event.source,
            "payload": event.payload,
        })

        if len(self._recent_points) > 256:
            self._recent_points.pop(0)

        self._recompute(event.frame)

    # ========================================================
    # Rolling access (FIX)
    # ========================================================

    def tail(self, n: int = 50) -> List[LedgerEvent]:
        """
        Return the last n ledger events.
        REQUIRED by Concierge / Manager layers.
        """
        return self.events[-n:]

    # ========================================================
    # Recompute gates
    # ========================================================

    def _recompute(self, frame: int):
        self.pattern_stability = min(1.0, 0.01 * len(self._recent_points))

        square_result = coherence_gate(self._recent_points, size=32)
        self.square_coherence = square_result

        square_c = float(square_result.get("coherence", 0.0))

        self.semantic_readiness = min(
            1.0,
            0.55 * self.pattern_stability +
            0.45 * square_c
        )

    # ========================================================
    # Snapshot
    # ========================================================

    def snapshot(self) -> Dict[str, Any]:
        return {
            "events": len(self.events),
            "pattern_stability": round(self.pattern_stability, 3),
            "square_coherence": self.square_coherence,
            "semantic_readiness": round(self.semantic_readiness, 3),
        }