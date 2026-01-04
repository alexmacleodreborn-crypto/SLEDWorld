from world_core.heartbeat_field import HeartbeatField


class BodyState:
    """
    Pre-symbolic bodily substrate.
    No concepts. No language. Only regulation.
    """

    def __init__(self):
        # Internal fetal heartbeat (subjective)
        self.internal_heartbeat = HeartbeatField(
            bpm=120,
            amplitude=0.6
        )

        # Primitive regulation states
        self.arousal = 0.0
        self.pressure = 0.5
        self.warmth = 0.7

    def tick(self, minutes: float = 1.0):
        """
        Advance internal bodily processes.
        """
        self.internal_heartbeat.tick(minutes=minutes)

        # Homeostatic drift
        self.arousal *= 0.98
        self.pressure = max(0.0, min(1.0, self.pressure))
        self.warmth = max(0.0, min(1.0, self.warmth))

    def snapshot(self):
        return {
            "heartbeat_signal": self.internal_heartbeat.current_signal(),
            "arousal": round(self.arousal, 3),
            "pressure": round(self.pressure, 3),
            "warmth": round(self.warmth, 3),
        }