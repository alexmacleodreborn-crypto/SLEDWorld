# world_core/ledger.py

from typing import List, Dict, Any
from world_core.ledger_event import LedgerEvent
from world_core.sandys_square import coherence_gate

class Ledger:
    """
    Immutable record + Sandy’s Law gating.
    Not a bot. No perception. No action.
    """
    def __init__(self):
        self.events: List[LedgerEvent] = []

        # rolling metrics
        self.pattern_stability: float = 0.0
        self.structure_confidence: float = 0.0
        self.semantic_readiness: float = 0.0
        self.square_coherence: float = 0.0

        # derived gate state
        self.manager_approval: Dict[str, Any] = {}

        # caches
        self._entity_counts: Dict[str, int] = {}
        self._recent_points: List[tuple[int,int]] = []  # for square gate demo

    def ingest(self, ev: LedgerEvent):
        self.events.append(ev)

        self._entity_counts[ev.entity] = self._entity_counts.get(ev.entity, 0) + 1

        # Collect points if present (y,x) integer
        pt = ev.payload.get("point_yx")
        if isinstance(pt, (list, tuple)) and len(pt) == 2:
            self._recent_points.append((int(pt[0]), int(pt[1])))
            self._recent_points = self._recent_points[-300:]

        self._recompute(ev.frame)

    def tail(self, n=50) -> List[Dict[str, Any]]:
        t = self.events[-n:]
        return [{
            "frame": e.frame, "source": e.source, "entity": e.entity, "kind": e.kind,
            "confidence": e.confidence, "payload": e.payload
        } for e in t]

    # -------------------------
    # Sandy’s Law-style metrics
    # -------------------------
    def _recompute(self, frame: int):
        # Pattern stability: repetition of same entities
        total = len(self.events)
        if total == 0:
            return

        top = max(self._entity_counts.values()) if self._entity_counts else 0
        self.pattern_stability = min(1.0, top / max(10, total))

        # Structure confidence: do we have structure-like sources?
        structure_hits = sum(1 for e in self.events[-200:] if e.kind in ("structure", "survey"))
        self.structure_confidence = min(1.0, structure_hits / 60.0)

        # Square coherence from recent points
        # (this is your SandySquare gate signal)
        self.square_coherence = coherence_gate(self._recent_points, size=32)

        # Semantic readiness: needs stable patterns + coherence
        self.semantic_readiness = min(1.0, 0.55*self.pattern_stability + 0.45*self.square_coherence)

        # Z / Σ style gating (simple v1)
        # Σ ~ change density; Z ~ inhibition / structure
        Sigma = 1.0 - self.pattern_stability
        Z = self.square_coherence

        divergence = Sigma * Z
        coherence = 1.0 - divergence

        # Gates
        self.manager_approval = {
            "frame": frame,
            "Sigma": round(Sigma, 3),
            "Z": round(Z, 3),
            "divergence": round(divergence, 3),
            "coherence": round(coherence, 3),

            "patterns_stable": self.pattern_stability >= 0.20,
            "structure_confirmed": self.structure_confidence >= 0.30,
            "language_ready": self.semantic_readiness >= 0.35,
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "frame": self.events[-1].frame if self.events else 0,
            "pattern_stability": round(self.pattern_stability, 3),
            "structure_confidence": round(self.structure_confidence, 3),
            "square_coherence": round(self.square_coherence, 3),
            "semantic_readiness": round(self.semantic_readiness, 3),
            "manager_approval": self.manager_approval,
            "events_count": len(self.events),
        }