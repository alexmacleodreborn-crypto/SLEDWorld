class BodyState:
    """
    Autonomic, pre-symbolic body dynamics.
    No intentional actions live here.
    """

    def __init__(self):
        self.muscle_tone = 0.4
        self.movement_intensity = 0.2
        self.comfort = 0.7
        self.rhythm_stability = 0.8

    def apply_intensity(self, intensity: float):
        intensity = max(0.0, min(1.0, intensity))
        self.movement_intensity = (
            self.movement_intensity * 0.7 + intensity * 0.3
        )
        self.comfort = max(0.0, min(1.0, self.comfort - intensity * 0.05))
        self.rhythm_stability = max(
            0.0, min(1.0, self.rhythm_stability - intensity * 0.02)
        )

    def snapshot(self):
        """
        Observer-only body state snapshot.
        """
        return {
            "muscle_tone": round(self.muscle_tone, 2),
            "movement_intensity": round(self.movement_intensity, 2),
            "comfort": round(self.comfort, 2),
            "distress": round(1.0 - self.comfort, 2),
            "rhythm_stability": round(self.rhythm_stability, 2),
        }