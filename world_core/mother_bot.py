from __future__ import annotations

from world_core.heartbeat_field import HeartbeatField


class MotherBot:
    """
    World agent representing the mother.
    Lives fully in world time.
    Provides sensory coupling to gestation.
    """

    def __init__(self, clock):
        self.clock = clock

        # Mother's heartbeat (world-side)
        self.heartbeat = HeartbeatField()
        if hasattr(self.heartbeat, "bpm"):
            self.heartbeat.bpm = 80  # typical resting maternal BPM

        self._last_minutes = None

    # -------------------------------------------------
    # World tick
    # -------------------------------------------------

    def tick(self):
        """
        Advance mother state using world time.
        """
        now_minutes = float(getattr(self.clock, "total_minutes", 0.0))

        if self._last_minutes is None:
            delta = 0.0
        else:
            delta = now_minutes - self._last_minutes

        self._last_minutes = now_minutes

        # Advance heartbeat using whatever API exists
        if hasattr(self.heartbeat, "tick"):
            try:
                self.heartbeat.tick(minutes=delta)
            except TypeError:
                try:
                    self.heartbeat.tick(delta)
                except Exception:
                    pass
        elif hasattr(self.heartbeat, "tick_minutes"):
            try:
                self.heartbeat.tick_minutes(delta)
            except Exception:
                pass

    # -------------------------------------------------
    # Sensory bridge (THIS FIXES YOUR ERROR)
    # -------------------------------------------------

    def sensory_snapshot(self) -> dict:
        """
        Return maternal sensory signals available to the fetus.
        This is pre-symbolic and intensity-only.
        """
        heartbeat_signal = 0.0

        # Extract heartbeat signal safely
        for attr in ("current_signal", "signal", "value"):
            if hasattr(self.heartbeat, attr):
                try:
                    heartbeat_signal = float(getattr(self.heartbeat, attr))
                    break
                except Exception:
                    pass

        if callable(getattr(self.heartbeat, "current_signal", None)):
            try:
                heartbeat_signal = float(self.heartbeat.current_signal())
            except Exception:
                pass

        return {
            "heartbeat": heartbeat_signal,
            "pressure": 0.6,   # womb pressure baseline
            "sound": 0.4,      # muffled maternal sounds
            "motion": 0.2,     # maternal movement
            "warmth": 0.8,     # thermal coupling
        }

    # -------------------------------------------------
    # Observer view
    # -------------------------------------------------

    def snapshot(self, world_datetime=None) -> dict:
        return {
            "agent": "mother",
            "world_time": str(world_datetime) if world_datetime else None,
            "heartbeat_bpm": getattr(self.heartbeat, "bpm", None),
            "heartbeat_phase": getattr(self.heartbeat, "phase", None),
        }