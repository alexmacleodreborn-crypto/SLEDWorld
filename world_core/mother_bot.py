# sledworld/world_core/mother_bot.py

from world_core.heartbeat_field import HeartbeatField

class MotherBot:
    """
    Mother biological presence.
    Provides external sensory coupling during gestation.
    """

    def __init__(self):
        # Adult resting heart rate
        self.heartbeat = HeartbeatField(bpm=80, noise=0.08, seed=11)

    def tick(self, dt_seconds: float) -> dict:
        """
        Advance mother state.
        Returns sensory snapshot available to fetus.
        """
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