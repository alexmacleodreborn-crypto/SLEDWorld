# world_core/architect_bot.py

from __future__ import annotations
from typing import Dict, Any, List

class ArchitectBot:
    """
    Reads the ledger/symbols only.
    Proposes higher-level structure based on available evidence.
    Never confirms.
    """
    def propose(self, ledger) -> List[Dict[str, Any]]:
        proposals: List[Dict[str, Any]] = []

        symbols = getattr(ledger, "symbols", {}) or {}

        # Minimal stage-1 proposals:
        # If we have aerial map, propose WALL_CANDIDATE and ROOM_CANDIDATE
        if "AERIAL_MAP" in symbols and symbols["AERIAL_MAP"].get("confidence", 0) >= 0.7:
            proposals.append({
                "source": "architect",
                "proposal": "WALL",
                "reason": "aerial_map_present",
                "confidence": 0.6
            })
            proposals.append({
                "source": "architect",
                "proposal": "ROOM",
                "reason": "enclosure_possible_from_aerial",
                "confidence": 0.55
            })

        # If TV and ONOFF exist, propose OBJECT_STATEFUL
        if "TV" in symbols and "ONOFF" in symbols:
            proposals.append({
                "source": "architect",
                "proposal": "STATEFUL_OBJECT",
                "reason": "tv_onoff_detected",
                "confidence": 0.7
            })

        return proposals