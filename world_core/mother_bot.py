from world_core.heartbeat_field import HeartbeatField

class MotherBot:
    """
    Mother exists fully inside world time.
    A7DO never sees this directly.
    """

    def __init__(self, clock):
        self.clock = clock

        self.heartbeat = HeartbeatField(
            bpm_mean=72.0,
            bpm_variance=8.0,
            seed=21
        )

    def tick(self, minutes: float):
        """
        Advance physiological rhythm with world time.
        """
        return self.heartbeat.tick(minutes)

    def snapshot(self):
        """
        Observer-only diagnostic.
        """
        return {
            "world_time": self.clock.world_datetime.isoformat(),
            "heartbeat_level": round(self.heartbeat.last_level, 3),
        }