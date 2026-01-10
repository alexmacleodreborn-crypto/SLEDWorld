# world_core/language_bot.py

class LanguageBot:
    """
    Symbol ↔ sound ↔ meaning binder.
    No grammar. No sentences.
    Just grounded labels.
    """

    def __init__(self):
        self.name = "Language"
        self.lexicon = {}
        self.events = []

        self.min_repeats = 8

    def review(self, ledger):
        sound_hits = {}
        light_hits = {}

        for e in ledger.events[-400:]:
            if e.get("source") == "observer":
                seen = e.get("seen_objects", {})
                heard = e.get("heard", {})

                if "tv_is_on" in seen:
                    key = "TV"
                    sound_hits[key] = sound_hits.get(key, 0) + 1

                light = seen.get("tv_light_color")
                if light:
                    light_hits.setdefault(light, 0)
                    light_hits[light] += 1

        # --- Bind TV ---
        if sound_hits.get("TV", 0) >= self.min_repeats:
            self._bind("TV", {
                "function": "emits_sound_and_light",
                "light_colors": list(light_hits.keys()),
            })

    def _bind(self, word, meaning):
        if word in self.lexicon:
            return
        self.lexicon[word] = meaning
        self.events.append({
            "source": "language",
            "word": word,
            "meaning": meaning,
        })

    def snapshot(self):
        return {
            "source": "language",
            "lexicon": self.lexicon,
            "events": self.events[-10:],
        }