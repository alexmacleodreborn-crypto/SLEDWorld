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

    This is the ONLY unit the Manager reasons over.
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

    Responsibilities:
    - Store all events
    - Track pattern stability
    - Run SandySquare coherence gating
    - Expose semantic readiness for Manager approval
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
        """
        Add an event to the ledger and recompute gates.
        """
        self.events.append(event)

        # Track minimal spatial / symbolic points for SandySquare
        point = {
            "source": event.source,
            "payload": event.payload,
        }
        self._recent_points.append(point)

        # Limit rolling window
        if len(self._recent_points) > 256:
            self._recent_points.pop(0)

        # Recompute gates
        self._recompute(event.frame)

    # ========================================================
    # Recompute gates
    # ========================================================

    def _recompute(self, frame: int):
        """
        Recompute pattern stability and SandySquare coherence.

        IMPORTANT:
        SandySquare returns a PHYSICS PACKET (dict),
        not a scalar. We must extract coherence explicitly.
        """

        # --------------------------------------------
        # Pattern stability (simple accumulation)
        # --------------------------------------------
        self.pattern_stability = min(
            1.0,
            0.01 * len(self._recent_points)
        )

        # --------------------------------------------
        # SandySquare gate (FULL RESULT)
        # --------------------------------------------
        square_result = coherence_gate(
            self._recent_points,
            size=32
        )

        # Store full physics packet
        self.square_coherence = square_result

        # Extract scalar coherence safely
        square_c = float(square_result.get("coherence", 0.0))

        # --------------------------------------------
        # Semantic readiness (FINAL scalar)
        # --------------------------------------------
        self.semantic_readiness = min(
            1.0,
            0.55 * float(self.pattern_stability) +
            0.45 * square_c
        )

    # ========================================================
    # Snapshot (for Streamlit / Manager)
    # ========================================================

    def snapshot(self) -> Dict[str, Any]:
        return {
            "events": len(self.events),
            "pattern_stability": round(self.pattern_stability, 3),
            "square_coherence": self.square_coherence,
            "semantic_readiness": round(self.semantic_readiness, 3),
        }