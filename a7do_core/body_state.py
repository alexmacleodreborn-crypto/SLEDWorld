from experience_layer.heartbeat_field import HeartbeatField


class BodyState:
    """
    Pre-symbolic bodily substrate.
    No concepts, no language, only regulation.
    """

    def __init__(self):
        # Internal heartbeat (subjective, fetal → infant)
        self.internal_heartbeat = HeartbeatField(
            bpm=120,        # fetal baseline
            amplitude=0.6
        )

        # Primitive regulation states
        self.arousal = 0.0
        self.pressure = 0.5
        self.warmth = 0.7

    # --------------------------------------------------
    # REQUIRED METHOD (THIS FIXES YOUR CRASH)
    # --------------------------------------------------

    def tick(self, minutes: float = 1.0):
        """
        Advance internal bodily processes.
        Called every gestation / wake tick.
        """
        # Heartbeat progresses independently of world meaning
        try:
            self.internal_heartbeat.tick(minutes=minutes)
        except TypeError:
            # fallback if API differs
            self.internal_heartbeat.tick(minutes)

        # Gentle homeostasis drift
        self.arousal *= 0.98
        self.pressure = min(1.0, max(0.0, self.pressure))
        self.warmth = min(1.0, max(0.0, self.warmth))

    # --------------------------------------------------
    # Observer-only view
    # --------------------------------------------------

    def snapshot(self):
        return {
            "heartbeat_signal": (
                self.internal_heartbeat.current_signal()
                if hasattr(self.internal_heartbeat, "current_signal")
                else None
            ),
            "arousal": round(self.arousal, 3),
            "pressure": round(self.pressure, 3),
            "warmth": round(self.warmth, 3),
        }