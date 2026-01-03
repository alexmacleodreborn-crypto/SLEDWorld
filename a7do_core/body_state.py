class BodyState:
    def __init__(self):
        self.arousal = 0.0

    def apply_intensity(self, intensity):
        self.arousal += intensity