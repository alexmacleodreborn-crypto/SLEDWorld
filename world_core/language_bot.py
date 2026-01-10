# world_core/language_bot.py

class LanguageBot:
    """
    Symbol compiler.
    Reads stable patterns from ledger and assigns tokens (TV, ON, OFF, BRICK, WALL).
    Stage-0: token assignment from persistence + deltas.
    """

    def __init__(self, name="Language-1"):
        self.name = name
        self.last_snapshot = {"source": "language", "name": self.name, "tokens": []}

    def observe(self, world):
        ledger = getattr(world, "salience_investigator", None)
        entries = getattr(ledger, "ledger", []) if ledger else []

        # Look for repeated TV signal changes (sound/light)
        tv_events = [e for e in entries if isinstance(e, dict) and e.get("target") == "tv"]
        sound = [e for e in tv_events if e.get("focus") == "sound"]
        light = [e for e in tv_events if e.get("focus") == "light"]

        tokens = []
        if len(sound) > 5:
            tokens.append({"token": "TV_SOUND_SIGNATURE", "confidence": 0.6})
        if len(light) > 5:
            tokens.append({"token": "TV_LIGHT_SIGNATURE", "confidence": 0.6})

        # ON/OFF emerges from alternating delta
        # (very simple heuristic for now)
        if any(e.get("delta") == 1 for e in sound) and any(e.get("delta") == 0 for e in sound):
            tokens.append({"token": "ON_OFF_STATE", "confidence": 0.5})

        self.last_snapshot = {
            "source": "language",
            "name": self.name,
            "frame": getattr(world, "frame", None),
            "tokens": tokens
        }

    def snapshot(self):
        return self.last_snapshot