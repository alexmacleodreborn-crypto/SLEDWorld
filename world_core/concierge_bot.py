# world_core/concierge_bot.py

from typing import List
from world_core.ledger import LedgerEvent


class ConciergeBot:
    """
    Proposal layer.

    - Reads recent ledger events
    - Groups them into candidate 'meaning bundles'
    - Forwards stable bundles to Manager
    """

    def __init__(self):
        self.last_proposal = None

    # =========================================================
    # Propose meaning from ledger events
    # =========================================================

    def propose(self, events: List[LedgerEvent]):
        """
        Accepts LedgerEvent objects (NOT dicts).
        """

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
            # --- typed access (FIX) ---
            payload = e.payload or {}

            bundle["frames"].append(e.frame)
            bundle["sources"].add(e.source)

            # --- signal detection ---
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

        self.last_proposal = bundle
        return bundle

    # =========================================================
    # Snapshot
    # =========================================================

    def snapshot(self):
        return {
            "active": True,
            "last_proposal": self.last_proposal,
        }