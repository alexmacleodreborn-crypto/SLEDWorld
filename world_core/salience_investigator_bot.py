# world_core/salience_investigator_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SalienceInvestigatorBot:
    """
    Accounting layer.
    - Ingests snapshots from any source (observer, walker, scout, world_space)
    - Emits a flat ledger of transactions (raw for now)
    - Later: rules deploy scouts based on thresholds (you can extend)
    """
    name: str = "Investigator-1"
    frame_counter: int = 0
    ledger: List[Dict[str, Any]] = field(default_factory=list)

    def ingest(self, snap: Dict[str, Any]):
        if not isinstance(snap, dict):
            return

        src = snap.get("source", "unknown")
        frame = snap.get("frame", None)

        # Update internal frame counter (best-effort)
        if isinstance(frame, int) and frame >= self.frame_counter:
            self.frame_counter = frame

        tx = {
            "tx_type": "ingest",
            "source": src,
            "frame": frame,
            "data": snap,
        }
        self.ledger.append(tx)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "source": "salience_investigator",
            "frame_counter": self.frame_counter,
            "total_transactions": len(self.ledger),
            "tail_sources": [t.get("source") for t in self.ledger[-10:]],
        }