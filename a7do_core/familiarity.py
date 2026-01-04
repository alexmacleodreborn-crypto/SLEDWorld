from collections import defaultdict
import random


class Familiarity:
    """
    Pre-symbolic pattern exposure memory.
    Observer-visible but NOT accessible to A7DO.
    """

    def __init__(self, gated: bool = True, seed: int = 7):
        self.gated = gated
        self.rng = random.Random(seed)
        self.patterns = defaultdict(float)
        self.last_pattern = None

    def unlock(self):
        self.gated = False

    def observe(self, *, place: str, channels: dict, intensity: float):
        dominant = "ambient"
        if channels:
            dominant = max(channels.items(), key=lambda kv: float(kv[1]))[0]

        pattern = f"{place}:{dominant}"
        self.last_pattern = pattern

        weight = max(0.0, float(intensity))
        if self.gated:
            weight *= 0.35

        self.patterns[pattern] += weight

    def top(self, n: int = 5):
        """
        Observer-safe summary.
        Returns JSON-serialisable list.
        """
        return [
            {"pattern": k, "weight": round(v, 4)}
            for k, v in sorted(
                self.patterns.items(),
                key=lambda kv: kv[1],
                reverse=True
            )[:n]
        ]

    def snapshot(self):
        return {
            "gated": self.gated,
            "last_pattern": self.last_pattern,
            "top": self.top(),
        }