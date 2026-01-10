# world_core/language_bot.py

class LanguageBot:
    """
    Symbol → word promotion layer.

    Activated only after sufficient pattern stability.
    """

    def __init__(self):
        self.vocabulary = {}
        self.events = []

    # =================================================
    # Ingest Concierge proposals
    # =================================================

    def ingest_proposals(self, proposals):
        if not proposals:
            return []

        new_events = []

        for p in proposals:
            signals = p.get("signals", {})
            objects = p.get("objects", [])

            # Example: first grounded word
            if signals.get("light") and signals.get("sound") and "tv" in "".join(objects).lower():
                if "TV" not in self.vocabulary:
                    self.vocabulary["TV"] = {
                        "type": "object",
                        "grounded_in": "light+sound+shape",
                    }
                    ev = {
                        "word": "TV",
                        "reason": "repeated light+sound+shape correlation",
                    }
                    new_events.append(ev)
                    self.events.append(ev)

        return new_events

    # =================================================
    # Snapshot
    # =================================================

    def snapshot(self):
        return {
            "vocabulary": self.vocabulary,
            "events": self.events[-10:],
        }