# a7do_core/body_state.py

from world_core.heartbeat_field import HeartbeatField


class BodyState:
    """
    Subjective body state of A7DO.
    Has no concept of time, only rhythmic entrainment.
    """

    def __init__(self):
        # Internal heartbeat (entrained, not causal)
        self.internal_heartbeat = HeartbeatField(bpm=120.0)

        # Primitive proprioception placeholders
        self.tension = 0.0
        self.motion = 0.0

    def entrain(self, external_heartbeat_value):
        """
        Pre-birth coupling: internal rhythm follows mother.
        """
        self.internal_heartbeat.entrain(external_heartbeat_value)

    def snapshot(self):
        return {
            "heartbeat": self.internal_heartbeat.snapshot(),
            "tension": self.tension,
            "motion": self.motion,
        }