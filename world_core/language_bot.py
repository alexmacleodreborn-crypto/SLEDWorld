# world_core/language_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class LanguageBot:
    """
    Language = late-stage symbol-to-token mapping.
    Never reads world. Only reads symbols and transitions from the ledger.

    Produces:
      - lexicon: stable symbols -> tokens
      - utterances: minimal state statements like TV ON / TV OFF
    """

    name: str = "Language-1"
    lexicon: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    utterances: List[Dict[str, Any]] = field(default_factory=list)
    frame: int = 0

    def update(self, frame: int, symbols: Dict[str, Any], transitions: List[Dict[str, Any]]) -> None:
        self.frame = frame

        # Promote structural tokens when symbols exist
        for sym in ["BRICK", "WALL", "ROOM", "TV"]:
            if sym in symbols.get("types", {}):
                if sym not in self.lexicon:
                    self.lexicon[sym] = {
                        "token": sym,
                        "confidence": symbols["types"][sym].get("confidence", 0.8),
                        "first_frame": frame,
                    }

        # Convert transitions into minimal utterances
        for t in transitions[-30:]:
            if t.get("event") == "light_change":
                to = t.get("to", {})
                color = to.get("color", "none")
                # Map light color to ON/OFF for TV-like objects
                if color == "green":
                    self.utterances.append({"frame": t["frame"], "utterance": "TV ON"})
                    self.utterances.append({"frame": t["frame"], "utterance": "GREEN"})
                elif color == "red":
                    self.utterances.append({"frame": t["frame"], "utterance": "TV OFF"})
                    self.utterances.append({"frame": t["frame"], "utterance": "RED"})

            if t.get("event") == "sound_change":
                # Optional minimal statement
                frm = t.get("from", 0.0)
                to = t.get("to", 0.0)
                if to > frm:
                    self.utterances.append({"frame": t["frame"], "utterance": "SOUND RISE"})
                elif to < frm:
                    self.utterances.append({"frame": t["frame"], "utterance": "SOUND FALL"})

        # Keep utterances bounded
        if len(self.utterances) > 500:
            self.utterances = self.utterances[-500:]

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "language",
            "name": self.name,
            "frame": self.frame,
            "lexicon": self.lexicon,
            "utterances_tail": self.utterances[-25:],
        }