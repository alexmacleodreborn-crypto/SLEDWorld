from world_core.heartbeat_field import HeartbeatField

class MotherBot:
    """
    World agent.
    Fully time-coupled to WorldClock.
    """

    def __init__(self, clock):
        self.clock = clock
        self.heartbeat = HeartbeatField(bpm=80.0)

    def tick(self):
        """
        Advance internal physiology using world delta time.
        """
        minutes = self.clock.delta_minutes
        self.heartbeat.tick(minutes)

    def snapshot(self, world_datetime):
        return {
            "world_time": world_datetime.isoformat(),
            "heartbeat_phase": round(self.heartbeat.phase, 4),
            "bpm": self.heartbeat.bpm,
        }