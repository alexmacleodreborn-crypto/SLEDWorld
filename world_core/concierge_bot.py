# world_core/concierge_bot.py

from typing import List
from world_core.ledger import LedgerEvent


class ConciergeBot:
    """
    Interpretation layer.

    - Reads ledger events
    - Proposes candidate meaning bundles
    - Maintains short proposal history
    """

    def __init__(self, tail_size: int = 50):
        self.last_proposal = None
        self.proposals_tail: List[dict] = []
        self.tail_size = int(tail_size)

    # =========================================================
    # Propose meaning from ledger events
    # =========================================================

    def propose(self, events: List[LedgerEvent]):
        if not events:
            self.last_proposal = None
            return None

        bundle = {
            "frames": [],
            "sources": set(),
            "objects": set(),
            "signals": {
                "sound": False,
                "light": False,
                "shape": False,
            }
        }

        for e in events:
            payload = e.payload or {}

            bundle["frames"].append(e.frame)
            bundle["sources"].add(e.source)

            if payload.get("sound_level", 0) > 0:
                bundle["signals"]["sound"] = True

            if payload.get("light_level", 0) > 0:
                bundle["signals"]["light"] = True

            if payload.get("shape_id"):
                bundle["signals"]["shape"] = True
                bundle["objects"].add(payload["shape_id"])

            if payload.get("object"):
                bundle["objects"].add(payload["object"])

        # normalise
        bundle["sources"] = sorted(bundle["sources"])
        bundle["objects"] = sorted(bundle["objects"])

        # store
        self.last_proposal = bundle
        self.proposals_tail.append(bundle)

        # trim history
        if len(self.proposals_tail) > self.tail_size:
            self.proposals_tail = self.proposals_tail[-self.tail_size :]

        return bundle

    # =========================================================
    # Snapshot
    # =========================================================

    def snapshot(self):
        return {
            "active": True,
            "last_proposal": self.last_proposal,
            "proposals_tail": self.proposals_tail[-10:],  # safe UI view
        }