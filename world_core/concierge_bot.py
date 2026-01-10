# world_core/concierge_bot.py
from typing import Dict, Any, List

class ConciergeBot:
    def __init__(self, name="Concierge-1"):
        self.name = name
        self.proposals: List[Dict[str, Any]] = []

    def propose(self, ledger_tail: List[Dict[str, Any]]):
        # Example: detect repeated TV state deltas or light/sound signatures
        tv_like = 0
        for e in ledger_tail:
            p = e.get("payload", {})
            if p.get("tv_state") is not None or p.get("seen_light_color") in ("red","green"):
                tv_like += 1
        if tv_like >= 6:
            self.proposals.append({"symbol_candidate":"TV","confidence":0.7,"reason":"repeated light/sound state signatures"})

    def proposals_tail(self, n=20):
        return self.proposals[-n:]

    def snapshot(self):
        return {"source":"concierge","name":self.name,"proposals_tail": self.proposals[-20:]}