class BodyState:
    """
    Physiological substrate.
    No cognition. No symbols. No time awareness.
    """

    def __init__(self):
        # Core arousal state
        self.awake = False

        # Baseline physiology
        self.arousal = 0.1
        self.fatigue = 0.0

    # -----------------------------
    # BODY TRANSITIONS
    # -----------------------------

    def wake(self):
        self.awake = True
        self.arousal = min(1.0, self.arousal + 0.4)
        self.fatigue = max(0.0, self.fatigue - 0.2)

    def sleep(self):
        self.awake = False
        self.arousal = max(0.0, self.arousal - 0.3)
        self.fatigue = min(1.0, self.fatigue + 0.2)

    # -----------------------------
    # BODY TICK (optional)
    # -----------------------------

    def tick(self):
        if self.awake:
            self.fatigue = min(1.0, self.fatigue + 0.01)
        else:
            self.fatigue = max(0.0, self.fatigue - 0.02)

    # -----------------------------
    # OBSERVER SNAPSHOT
    # -----------------------------

    def snapshot(self):
        return {
            "awake": self.awake,
            "arousal": round(self.arousal, 3),
            "fatigue": round(self.fatigue, 3),
        }