class ConciergeBot:
    """
    Proposes symbol candidates from stable ledger evidence.
    Dormant unless called.
    """
    def __init__(self):
        self._proposals = []

    def propose(self, ledger_tail):
        # ledger_tail is list[dict]
        # naive: if we see repeated walker interactions + peaks, propose "object_candidate"
        w = sum(1 for e in ledger_tail if e.get("kind") == "walker_interaction")
        s = sum(1 for e in ledger_tail if e.get("kind") == "sound_peaks")
        l = sum(1 for e in ledger_tail if e.get("kind") == "light_peaks")

        if w >= 3 and (s + l) >= 5:
            self._proposals.append({
                "source": "concierge",
                "proposal_type": "symbol_candidate",
                "symbol_candidate": {
                    "kind": "DEVICE",
                    "hint": "repeating toggle-correlated emitter",
                }
            })

        # keep tail short
        self._proposals = self._proposals[-50:]

    def proposals_tail(self, n=20):
        return self._proposals[-int(n):]