import math
from world_core.heartbeat_field import HeartbeatField


class MotherBot:
    """
    World agent representing the mother.
    Exists fully in world time.
    Provides heartbeat + ambient sensory coupling to gestation.
    """

    def __init__(self, clock):
        self.clock = clock

        # Maternal heartbeat (slower, stronger than foetal)
        self.heartbeat = HeartbeatField(
            bpm=80,            # typical resting maternal heart rate
            amplitude=1.0,
            name="mother"
        )

        self.last_tick_minutes = None

    def tick(self):
        """
        Advance mother state in world time.
        """
        # Determine elapsed world minutes since last tick
        now_minutes = self.clock.total_minutes
        if self.last_tick_minutes is None:
            delta = 0.0
        else:
            delta = now_minutes - self.last_tick_minutes

        self.last_tick_minutes = now_minutes

        if delta <= 0:
            return

        # ✅ CORRECT call — HeartbeatField supports tick(minutes=…)
        self.heartbeat.tick(minutes=delta)

    def snapshot(self, world_datetime=None):
        """
        Observer-visible state.
        """
        return {
            "agent": "mother",
            "world_time": str(world_datetime) if world_datetime else None,
            "heartbeat_bpm": self.heartbeat.bpm,
            "heartbeat_phase": round(self.heartbeat.phase, 3),
            "heartbeat_signal": round(self.heartbeat.current_signal(), 4),
        }