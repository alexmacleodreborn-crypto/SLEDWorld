# world_core/concierge_bot.py

from collections import defaultdict
from typing import Dict, Any, List, Tuple


class ConciergeBot:
    """
    Cross-reference & structuring bot.

    Responsibilities:
    - Correlate observations across agents
    - Understand spatial relations (gesture → coordinate)
    - Propose candidate structures (rooms, objects, floors)
    - NO authority to accept meaning
    """

    def __init__(self):
        self.proposals: List[Dict[str, Any]] = []
        self.frame_counter: int = 0

        # Temporary spatial aggregation
        self._spatial_clusters = defaultdict(list)

    # -------------------------------------------------
    # Ingest normalised ledger entry
    # -------------------------------------------------

    def ingest(self, snap: Dict[str, Any]):
        self.frame_counter += 1

        source = snap.get("source")
        if not source:
            return

        # Only process perception & survey data
        if source not in {"observer", "surveyor", "scout"}:
            return

        self._aggregate_spatial(snap)

    # -------------------------------------------------
    # Spatial aggregation
    # -------------------------------------------------

    def _aggregate_spatial(self, snap: Dict[str, Any]):
        """
        Group observations by approximate location.
        This is the 'gesture understanding' layer.
        """
        pos = snap.get("position_xyz") or snap.get("center_xyz")
        if not pos:
            return

        # Quantise space (gesture tolerance)
        key = (
            round(pos[0] / 2),
            round(pos[1] / 2),
            round(pos[2] / 2),
        )

        self._spatial_clusters[key].append(snap)

    # -------------------------------------------------
    # Proposal generation
    # -------------------------------------------------

    def generate_proposals(self) -> List[Dict[str, Any]]:
        proposals = []

        for key, snaps in self._spatial_clusters.items():
            if len(snaps) < 3:
                continue  # not enough evidence

            kinds = {s.get("source") for s in snaps}
            if "surveyor" in kinds and "observer" in kinds:
                proposals.append({
                    "type": "structure_candidate",
                    "cluster_key": key,
                    "evidence": snaps,
                    "frame": self.frame_counter,
                })

        self._spatial_clusters.clear()
        self.proposals.extend(proposals)
        return proposals

    # -------------------------------------------------
    # Snapshot
    # -------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "concierge",
            "frames_processed": self.frame_counter,
            "pending_proposals": len(self.proposals),
            "recent_proposals": self.proposals[-5:],
        }