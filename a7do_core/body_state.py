from experience_layer.heartbeat_field import HeartbeatField

class BodyState:
    """
    Pre-conscious body substrate.
    """

    def __init__(self):
        self.heartbeat = HeartbeatField(bpm=140)
        self.arousal = 0.0

    def apply_intensity(self, intensity: float):
        self.arousal = max(self.arousal, intensity)

    def snapshot(self, world_minutes: float):
        return {
            "heartbeat": self.heartbeat.sample(world_minutes),
            "arousal": round(self.arousal, 3)
        }