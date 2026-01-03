from world_core.heartbeat_field import HeartbeatField

class BodyState:
    """
    Pre-symbolic physiological body.
    """

    def __init__(self):
        # Internal heartbeat (faster, noisier)
        self.internal_heartbeat = HeartbeatField(
            bpm_mean=110.0,
            bpm_variance=20.0,
            seed=99
        )
        self.last_level = 0.0

    def entrain(self, external_heartbeat: float, minutes: float):
        """
        Entrain internal rhythm to external signal.
        """
        internal = self.internal_heartbeat.tick(minutes)
        self.last_level = (internal * 0.7) + (external_heartbeat * 0.3)

    def snapshot(self):
        return {
            "heartbeat_level": round(self.last_level, 3)
        }