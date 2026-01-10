# world_core/language_bot.py

from typing import Dict, Any, List

class LanguageBot:
    """
    Symbols first. Words later.
    Produces "symbol" events, not final truth.
    """
    def __init__(self, name="Language-1"):
        self.name = name
        self.symbols_proposed: List[Dict[str, Any]] = []
        self.symbols_accepted: List[str] = []

    def ingest_proposals(self, proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out = []
        for p in proposals:
            sym = p.get("symbol_candidate")
            if not sym:
                continue
            if sym in self.symbols_accepted:
                continue
            self.symbols_proposed.append(p)
            out.append({
                "source": "language",
                "entity": sym,
                "symbol": sym,
                "confidence": float(p.get("confidence", 0.5)),
                "reason": p.get("reason",""),
            })
        return out

    def accept(self, symbol: str):
        if symbol not in self.symbols_accepted:
            self.symbols_accepted.append(symbol)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source":"language",
            "name": self.name,
            "symbols_accepted": self.symbols_accepted,
            "symbols_proposed_tail": self.symbols_proposed[-20:],
        }