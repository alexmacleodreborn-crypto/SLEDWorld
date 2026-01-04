from world_core.heartbeat_field import HeartbeatField


class MotherBot:
    """
    World agent representing the mother.
    Lives fully in world time.
    Provides heartbeat signal to gestation.
    """

    def __init__(self, clock):
        self.clock = clock

        # HeartbeatField signature-compatible construction
        # (no name, no unsupported kwargs)
        self.heartbeat = HeartbeatField(
            bpm=80,          # maternal resting heart rate
            amplitude=1.0
        )

        self._last_minutes = None

    def tick(self):
        """
        Advance mother state using world time.
        """
        now_minutes = self.clock.total_minutes

        if self._last_minutes is None:
            delta = 0.0
        else:
            delta = now_minutes - self._last_minutes

        self._last_minutes = now_minutes

        if delta <= 0:
            return

        # Correct API usage
        self.heartbeat.tick(minutes=delta)

    def snapshot(self, world_datetime=None):
        """
        Observer-visible diagnostic state.
        """
        return {
            "agent": "mother",
            "world_time": str(world_datetime) if world_datetime else None,
            "heartbeat_bpm": self.heartbeat.bpm,
            "heartbeat_phase": round(self.heartbeat.phase, 4),
            "heartbeat_signal": round(self.heartbeat.current_signal(), 5),
        }