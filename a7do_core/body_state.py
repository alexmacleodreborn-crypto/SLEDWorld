# a7do_core/body_state.py

from experience_layer.heartbeat_field import HeartbeatField


class BodyState:
    """
    Internal physiological state of A7DO.
    Runs continuously pre-birth and post-birth.
    """

    def __init__(self):
        # Fetal / newborn heart rate
        self.heartbeat = HeartbeatField(
            bpm=130,
            noise=0.12,
            seed=3
        )
        self.last_intensity = 0.0

    def tick(self, dt_seconds: float):
        self.last_intensity = self.heartbeat.tick(dt_seconds)

    def snapshot(self) -> dict:
        return {
            "heartbeat_bpm": self.heartbeat.bpm,
            "heartbeat_intensity": round(self.last_intensity, 3),
        }