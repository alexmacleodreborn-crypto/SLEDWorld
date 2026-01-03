from experience_layer.heartbeat_field import HeartbeatField

class MotherBot:
    """
    Mother exists continuously in world time.
    """

    def __init__(self):
        self.heartbeat = HeartbeatField(bpm=80)

    def snapshot(self, world_minutes: float):
        return {
            "heartbeat": self.heartbeat.sample(world_minutes)
        }