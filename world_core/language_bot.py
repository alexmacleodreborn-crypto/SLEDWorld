# world_core/language_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class LanguageBot:
    """
    Grounded lexicon only.
    No grammar.
    No free language.
    Words bind only after symbol exists.
    """
    lexicon: Dict[str, str] = field(default_factory=dict)

    def bind_from_symbols(self, symbols: Dict[str, Dict[str, Any]]):
        # Minimal grounded bindings
        if "TV" in symbols:
            self.lexicon.setdefault("TV", "tv")
        if "WALL" in symbols:
            self.lexicon.setdefault("WALL", "wall")
        if "ROOM" in symbols:
            self.lexicon.setdefault("ROOM", "room")
        if "ON" in symbols:
            self.lexicon.setdefault("ON", "on")
        if "OFF" in symbols:
            self.lexicon.setdefault("OFF", "off")
        if "COLOR_RED" in symbols:
            self.lexicon.setdefault("COLOR_RED", "red")
        if "COLOR_GREEN" in symbols:
            self.lexicon.setdefault("COLOR_GREEN", "green")
        if "SOUND_FIELD" in symbols:
            self.lexicon.setdefault("SOUND_FIELD", "sound")
        if "LIGHT_FIELD" in symbols:
            self.lexicon.setdefault("LIGHT_FIELD", "light")

    def snapshot(self) -> Dict[str, Any]:
        return {
            "lexicon": self.lexicon,
            "num_words": len(self.lexicon),
        }