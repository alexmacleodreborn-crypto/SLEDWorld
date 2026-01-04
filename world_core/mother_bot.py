# world_core/mother_bot.py

from world_core.heartbeat_field import HeartbeatField


class MotherBot:
    """
    World agent representing the mother.
    Exists fully in world time.
    """

    def __init__(self, clock):
        self.clock = clock

        # World-physics heartbeat (mother)
        self.heartbeat = HeartbeatField(bpm=80.0)

        # Sensory channels perceivable by fetus
        self.motion_level = 0.2
        self.voice_activity = 0.05
        self.digestive_activity = 0.1

        self._last_world_minutes = self.clock.total_minutes

    # --------------------------------------------------
    # WORLD TIME TICK
    # --------------------------------------------------

    def tick(self):
        now = self.clock.total_minutes
        delta = now - self._last_world_minutes
        self._last_world_minutes = now

        if delta <= 0:
            return

        # Advance mother heartbeat in world time
        self.heartbeat.tick_minutes(delta)

    # --------------------------------------------------
    # SENSORY OUTPUT (pre-birth coupling)
    # --------------------------------------------------

    def sensory_snapshot(self):
        """
        Sensory signal emitted into gestation.
        """
        return {
            "heartbeat": self.heartbeat.amplitude(),
            "motion": self.motion_level,
            "voice": self.voice_activity,
            "digestive": self.digestive_activity,
        }

    # --------------------------------------------------
    # OBSERVER VIEW
    # --------------------------------------------------

    def snapshot(self, world_datetime):
        return {
            "world_time": str(world_datetime),
            "heartbeat": self.heartbeat.snapshot(),
            "motion_level": self.motion_level,
            "voice_activity": self.voice_activity,
            "digestive_activity": self.digestive_activity,
        }