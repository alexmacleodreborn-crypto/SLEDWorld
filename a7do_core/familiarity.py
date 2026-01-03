from collections import defaultdict
import random

class Familiarity:
    """
    Pre-symbolic pattern exposure memory.
    Gated prebirth: records patterns at lower weight.
    """

    def __init__(self, gated: bool = True, seed: int = 7):
        self.gated = gated
        self.rng = random.Random(seed)
        self.patterns = defaultdict(float)
        self.last_pattern = "—"

    def unlock(self):
        self.gated = False

    def observe(self, *, place: str, channels: dict, intensity: float):
        # Create a stable pattern token (pre-language)
        # Keep it coarse: place + dominant channel.
        dominant = "ambient"
        if channels:
            dominant = max(channels.items(), key=lambda kv: float(kv[1]))[0]

        pat = f"{place}:{dominant}"
        self.last_pattern = pat

        weight = max(0.0, float(intensity))
        if self.gated:
            weight *= 0.35  # prebirth muted imprinting

        self.patterns[pat] += weight

    def top(self, n: int = 5):
        return sorted(self.patterns.items(), key=lambda kv: kv[1], reverse=True)[:n]

    def replay(self, n: int = 5):
        """
        Sleep replay: choose top patterns and reinforce lightly.
        Returns list of replayed patterns (observer-visible).
        """
        top = self.top(n)
        replayed = []
        for pat, score in top:
            bump = 0.15 if not self.gated else 0.05
            self.patterns[pat] += bump
            replayed.append(pat)
        return replayed