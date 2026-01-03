import random
import math
import time

class BodyState:
    """
    Pre-symbolic somatic state.
    Handles reflexive movement and internal rhythms.
    """

    def __init__(self):
        self.intensity = 0.0

        # Body regions with activation level
        self.regions = {
            "head": 0.0,
            "torso": 0.0,
            "left_arm": 0.0,
            "right_arm": 0.0,
            "left_leg": 0.0,
            "right_leg": 0.0,
        }

        # Proprioceptive familiarity
        self.movement_familiarity = {k: 0.0 for k in self.regions}

        # 🫀 Internal heartbeat (never stops)
        self._hb_phase = random.uniform(0, 2 * math.pi)
        self._hb_rate = random.uniform(1.2, 1.6)  # Hz (fetal / infant range)

    def apply_intensity(self, value: float):
        self.intensity = float(value)

    def reflex_move(self):
        region = random.choice(list(self.regions.keys()))
        amount = random.uniform(0.1, 0.4)

        self.regions[region] += amount
        self.movement_familiarity[region] += 0.2

        return region, amount

    def internal_heartbeat(self):
        """
        Generates a continuous internal rhythmic signal.
        Returns a low-amplitude pulse.
        """
        self._hb_phase += self._hb_rate * 0.1
        pulse = abs(math.sin(self._hb_phase)) * 0.15
        self.regions["torso"] += pulse
        return pulse