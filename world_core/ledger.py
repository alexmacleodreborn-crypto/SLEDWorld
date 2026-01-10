from dataclasses import dataclass, asdict
from typing import Dict, Any, List
from world_core.sandys_square import coherence_gate

@dataclass
class LedgerEvent:
    frame: int
    source: str
    kind: str
    payload: Dict[str, Any]

    def to_dict(self):
        return asdict(self)

class Ledger:
    """
    Stores events and computes Sandy gates from numeric evidence.
    """
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self._recent_points = []  # for SandySquare coherence
        self._max_points = 400

        # gates + scores
        self.object_stability = 0.0
        self.structure_stability = 0.0
        self.symbol_readiness = 0.0
        self.language_readiness = 0.0

        self.object_stable = False
        self.structure_stable = False
        self.symbol_ready = False
        self.language_ready = False

    def ingest(self, ev: LedgerEvent):
        d = ev.to_dict()
        self.events.append(d)

        # Collect “reaction points” from sensors:
        # - walker interactions
        # - scout peaks
        # - surveyor surface hits
        p = d.get("payload", {})
        pts = p.get("points_xy")
        if isinstance(pts, list):
            for xy in pts:
                if isinstance(xy, (list, tuple)) and len(xy) == 2:
                    self._recent_points.append((int(xy[0]), int(xy[1])))

        if len(self._recent_points) > self._max_points:
            self._recent_points = self._recent_points[-self._max_points:]

    def tail(self, n=50):
        return self.events[-int(n):]

    def recompute_gates(self):
        # coherence from SandySquare (0..1)
        coh = coherence_gate(self._recent_points, grid_size=32)

        # crude stability proxies:
        #  - object stability rises when we see repeated interaction + correlated field peaks
        #  - structure stability rises when surveyor produces consistent surface points
        #  - symbol readiness rises when object stability and coherence are high
        #  - language readiness rises later

        recent = self.tail(200)

        walker_hits = sum(1 for e in recent if e["kind"] == "walker_interaction")
        sound_hits = sum(1 for e in recent if e["kind"] == "sound_peaks")
        light_hits = sum(1 for e in recent if e["kind"] == "light_peaks")
        surf_hits = sum(1 for e in recent if e["kind"] == "surface_points")

        # normalize to 0..1
        self.object_stability = min(1.0, 0.25*min(1.0, walker_hits/6) + 0.25*min(1.0, sound_hits/8) + 0.25*min(1.0, light_hits/8) + 0.25*coh)
        self.structure_stability = min(1.0, 0.6*min(1.0, surf_hits/10) + 0.4*coh)

        self.symbol_readiness = min(1.0, 0.65*self.object_stability + 0.35*coh)
        self.language_readiness = min(1.0, 0.55*self.symbol_readiness + 0.45*self.structure_stability)

        # thresholds
        self.object_stable = self.object_stability >= 0.55
        self.structure_stable = self.structure_stability >= 0.55
        self.symbol_ready = self.symbol_readiness >= 0.60
        self.language_ready = self.language_readiness >= 0.75

    def gates_snapshot(self):
        return {
            "object_stability": float(self.object_stability),
            "structure_stability": float(self.structure_stability),
            "symbol_readiness": float(self.symbol_readiness),
            "language_readiness": float(self.language_readiness),
            "object_stable": bool(self.object_stable),
            "structure_stable": bool(self.structure_stable),
            "symbol_ready": bool(self.symbol_ready),
            "language_ready": bool(self.language_ready),
        }