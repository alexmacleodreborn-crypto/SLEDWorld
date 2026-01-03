from experience_layer.heartbeat_field import HeartbeatField


class MotherBot:
    """
    Mother biological agent.
    Exists in world time, independent of A7DO awareness.
    """

    def __init__(self):
        # Adult resting heartbeat ~70–80 bpm
        self.heartbeat = HeartbeatField(
            bpm=78,
            amplitude=1.0,
            source="mother"
        )

        self.state = {
            "location": "home",
            "activity": "resting",
        }

    def tick(self, dt_seconds: float):
        """
        Advance mother physiology in world time.
        """
        self.heartbeat.tick(dt_seconds)

    def snapshot(self):
        return {
            "heartbeat": self.heartbeat.snapshot(),
            "state": self.state,
        }