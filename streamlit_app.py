# world_core/mother_bot.py

from a7do_core.heartbeat_field import HeartbeatField


class MotherBot:
    """
    Embodied world agent representing the mother.
    Runs on world time, not A7DO time.
    """

    def __init__(self, clock):
        self.clock = clock

        # Physiological systems
        self.heartbeat = HeartbeatField(bpm=80.0)  # maternal heart rate

        # Sensory emission channels (what fetus can sense)
        self.motion_level = 0.2        # walking / shifting
        self.voice_activity = 0.05     # muffled speech
        self.digestive_activity = 0.1  # stomach sounds

        # Internal time tracking
        self._last_world_minutes = self.clock.total_minutes

    # --------------------------------------------------
    # WORLD TIME TICK
    # --------------------------------------------------

    def tick(self):
        """
        Advance mother physiology based on world time.
        """
        now = self.clock.total_minutes
        delta = now - self._last_world_minutes
        self._last_world_minutes = now

        if delta <= 0:
            return

        # Advance heartbeat using world minutes
        self.heartbeat.tick_minutes(delta)

        # Slow biological drift (life noise)
        self.motion_level = min(1.0, max(0.0, self.motion_level))
        self.voice_activity = min(0.3, max(0.0, self.voice_activity))
        self.digestive_activity = min(0.3, max(0.0, self.digestive_activity))

    # --------------------------------------------------
    # SENSORY OUTPUT (to gestation bridge)
    # --------------------------------------------------

    def sensory_snapshot(self):
        """
        What A7DO can sense from mother pre-birth.
        """
        return {
            "heartbeat": self.heartbeat.amplitude(),
            "motion": self.motion_level,
            "voice": self.voice_activity,
            "digestive": self.digestive_activity,
        }

    # --------------------------------------------------
    # OBSERVER SNAPSHOT
    # --------------------------------------------------

    def snapshot(self, world_datetime):
        return {
            "world_time": str(world_datetime),
            "heartbeat": self.heartbeat.snapshot(),
            "motion_level": round(self.motion_level, 3),
            "voice_activity": round(self.voice_activity, 3),
            "digestive_activity": round(self.digestive_activity, 3),
        }