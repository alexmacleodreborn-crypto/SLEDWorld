import random
from world_core.heartbeat_field import HeartbeatField


class MotherBot:
    """
    World agent: Mother.
    Exists fully in world time.
    """

    def __init__(self, clock):
        self.clock = clock
        self.agent = "mother"

        # Heartbeat (already working)
        self.heartbeat = HeartbeatField(
            bpm=80,
            variability=5,
            seed=11,
        )

        # Movement state (world-side only)
        self.position = 0.0
        self.velocity = 0.0

        self.rng = random.Random(21)

    # -----------------------------------------
    # WORLD TICK
    # -----------------------------------------

    def tick(self):
        """
        Advances mother's physical state in world time.
        """
        # Heartbeat advances with world time
        self.heartbeat.tick_minutes(15)

        # Slow, human-scale movement
        accel = self.rng.uniform(-0.02, 0.02)
        self.velocity += accel
        self.velocity *= 0.95  # damping
        self.position += self.velocity

    # -----------------------------------------
    # SENSORY SNAPSHOT (for gestation bridge)
    # -----------------------------------------

    def sensory_snapshot(self):
        """
        Returns pre-symbolic signals for fetus.
        """
        return {
            "heartbeat": self.heartbeat.current(),
            "motion": abs(self.velocity),
            "pressure": min(1.0, abs(self.velocity) * 2.0),
        }

    # -----------------------------------------
    # OBSERVER VIEW
    # -----------------------------------------

    def snapshot(self, world_datetime):
        return {
            "agent": self.agent,
            "world_time": str(world_datetime),
            "heartbeat_bpm": self.heartbeat.bpm,
            "heartbeat_phase": round(self.heartbeat.phase, 3),
            "velocity": round(self.velocity, 3),
            "position": round(self.position, 3),
        }