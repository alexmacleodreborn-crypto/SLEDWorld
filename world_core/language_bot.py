class LanguageBot:
    """
    Turns proposals into early symbol tokens.
    Dormant unless called.
    """
    def __init__(self):
        self.accepted_symbols = []
        self._emitted = []

    def ingest_proposals(self, proposals):
        self._emitted = []
        for p in proposals:
            cand = p.get("symbol_candidate")
            if not cand:
                continue

            # emit a pre-word token (symbol only)
            self._emitted.append({
                "source": "language",
                "event": "symbol_emitted",
                "symbol": cand,
            })

        return self._emitted

    def accept(self, symbol):
        self.accepted_symbols.append(symbol)

    def snapshot(self):
        return {
            "source": "language",
            "accepted_symbols": self.accepted_symbols[-10:]
        }