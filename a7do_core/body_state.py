from experience_layer.heartbeat_field import HeartbeatField


class BodyState:
    """
    Continuous physiological substrate.
    Exists pre-birth and post-birth.
    """

    def __init__(self):
        # A7DO's own internal heartbeat
        self.heartbeat = HeartbeatField(
            bpm=120,          # infant baseline
            amplitude=0.6,
            source="a7do"
        )

        self.intensity = 0.0

        # Proprioceptive presence (not yet semantic)
        self.parts = {
            "head": 0.0,
            "chest": 0.0,
            "left_arm": 0.0,
            "right_arm": 0.0,
            "left_leg": 0.0,
            "right_leg": 0.0,
        }

    def tick(self, dt_seconds: float):
        self.heartbeat.tick(dt_seconds)
        self.intensity = self.heartbeat.current_value

    def apply_intensity(self, value: float):
        self.intensity += float(value)

    def snapshot(self):
        return {
            "heartbeat": self.heartbeat.snapshot(),
            "intensity": round(self.intensity, 3),
            "parts": self.parts,
        }