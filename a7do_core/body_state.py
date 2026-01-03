# a7do_core/body_state.py

class BodyState:
    """
    Low-level physiological and somatic state.
    Non-symbolic, partially autonomous.
    """

    def __init__(self):
        # Core biological rhythms
        self.heart_rate = 120          # newborn baseline
        self.breath_rate = 40
        self.temperature = 36.8

        # Sensory discomfort / drive states
        self.hunger = 0.2
        self.wetness = 0.0
        self.fatigue = 0.1

        # Pain & touch (non-verbal)
        self.pain_level = 0.0
        self.touch_pressure = 0.0

        # Motor activity (pre-conscious)
        self.motor_activity = {
            "left_arm": 0.0,
            "right_arm": 0.0,
            "left_leg": 0.0,
            "right_leg": 0.0,
            "neck": 0.0,
        }

    def apply_intensity(self, intensity: float):
        """
        Generic physiological response to high-intensity events.
        """
        self.heart_rate = min(200, self.heart_rate + intensity * 15)
        self.breath_rate = min(80, self.breath_rate + intensity * 5)
        self.fatigue = min(1.0, self.fatigue + intensity * 0.1)

    def tick(self):
        """
        Passive decay toward baseline.
        """
        self.heart_rate += (120 - self.heart_rate) * 0.05
        self.breath_rate += (40 - self.breath_rate) * 0.05
        self.fatigue = max(0.0, self.fatigue - 0.02)
        self.hunger = min(1.0, self.hunger + 0.01)

    def snapshot(self):
        """
        Observer-safe representation of body state.
        """
        return {
            "heart_rate": round(self.heart_rate, 1),
            "breath_rate": round(self.breath_rate, 1),
            "temperature": self.temperature,
            "hunger": round(self.hunger, 2),
            "wetness": round(self.wetness, 2),
            "fatigue": round(self.fatigue, 2),
            "pain_level": round(self.pain_level, 2),
            "touch_pressure": round(self.touch_pressure, 2),
            "motor_activity": {
                k: round(v, 2) for k, v in self.motor_activity.items()
            },
        }