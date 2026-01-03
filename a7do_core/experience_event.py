class ExperienceEvent:
    """
    Atomic sensory experience.
    """

    def __init__(self, *, place: str, channels: dict, intensity: float):
        self.place = place
        self.channels = channels
        self.intensity = intensity