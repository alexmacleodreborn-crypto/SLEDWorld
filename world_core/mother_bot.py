# world_core/mother_bot.py

from experience_layer.heartbeat_field import HeartbeatField


class MotherBot:
    """
    Mother biological presence.
    External heartbeat + sensory field.
    """

    def __init__(self):
        self.heartbeat = HeartbeatField(
            bpm=80,
            noise=0.08,
            seed=11
        )

    def tick(self, dt_seconds: float) -> dict:
        hb = self.heartbeat.tick(dt_seconds)

        return {
            "heartbeat": hb,
            "muffled_sound": hb * 0.6,
            "pressure": 0.4,
            "warmth": 0.7,
        }

    def snapshot(self):
        return {
            "role": "mother",
            "heartbeat_bpm": self.heartbeat.bpm,
        }