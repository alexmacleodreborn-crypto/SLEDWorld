# sledworld/a7do_core/body_state.py

from world_core.heartbeat_field import HeartbeatField

class BodyState:
    """
    Internal physiological state of A7DO.
    Runs continuously regardless of awareness.
    """

    def __init__(self):
        # Fetal / newborn heart rate
        self.heartbeat = HeartbeatField(bpm=130, noise=0.12, seed=3)
        self.last_intensity = 0.0

    def tick(self, dt_seconds: float):
        self.last_intensity = self.heartbeat.tick(dt_seconds)

    def snapshot(self):
        return {
            "heartbeat_intensity": round(self.last_intensity, 3),
            "heartbeat_bpm": self.heartbeat.bpm,
        }