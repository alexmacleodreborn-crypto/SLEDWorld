from a7do_core.heartbeat_field import HeartbeatField


class MotherBot:
    """
    Embodied world agent.
    Represents mother as continuous presence.
    """

    def __init__(self, clock):
        self.clock = clock

        # Physiological systems
        self.heartbeat = HeartbeatField(bpm=80.0)   # adult resting
        self.breathing_rate = 14.0                  # breaths per minute

        # Sensory emission (what fetus perceives)
        self.motion_level = 0.2                     # walking / shifting
        self.voice_activity = 0.05                  # muffled speech
        self.digestive_activity = 0.1               # stomach sounds

        # Internal tracking
        self._last_clock_minutes = self.clock.total_minutes

    # --------------------------------------------------
    # WORLD-DRIVEN TICK
    # --------------------------------------------------

    def tick(self):
        """
        Advance mother state based on world time.
        """
        now_minutes = self.clock.total_minutes
        delta = now_minutes - self._last_clock_minutes
        self._last_clock_minutes = now_minutes

        if delta <= 0:
            return

        # Advance physiology
        self.heartbeat.tick_minutes(delta)

        # Slowly vary activity (life is noisy)
        self.motion_level = min(1.0, max(0.0, self.motion_level + 0.01))
        self.voice_activity = min(0.3, max(0.0, self.voice_activity + 0.005))
        self.digestive_activity = min(0.3, max(0.0, self.digestive_activity + 0.003))

    # --------------------------------------------------
    # SENSORY OUTPUT (to gestation bridge)
    # --------------------------------------------------

    def sensory_snapshot(self):
        """
        What A7DO can sense from mother (pre-birth).
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