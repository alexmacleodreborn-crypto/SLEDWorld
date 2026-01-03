from collections import defaultdict

class Familiarity:
    """
    Pre-symbolic exposure memory.
    """

    def __init__(self, gated: bool = True):
        self.gated = gated
        self.patterns = defaultdict(float)
        self.last_pattern = "—"

    def unlock(self):
        self.gated = False

    def observe(self, *, place: str, channels: dict, intensity: float):
        dominant = max(channels.items(), key=lambda x: x[1])[0]
        token = f"{place}:{dominant}"
        self.last_pattern = token

        weight = intensity * (0.35 if self.gated else 1.0)
        self.patterns[token] += weight

    def replay(self):
        for k in list(self.patterns.keys()):
            self.patterns[k] *= 1.02