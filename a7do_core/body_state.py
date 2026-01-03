class BodyState:
    """
    Low-level somatic state.
    This is NOT cognition.
    This is reflexive, local, pre-symbolic.
    """

    def __init__(self):
        self.intensity = 0.0
        self.regions = {
            "head": 0.0,
            "torso": 0.0,
            "left_arm": 0.0,
            "right_arm": 0.0,
            "left_leg": 0.0,
            "right_leg": 0.0,
        }

    def apply_intensity(self, value: float):
        self.intensity = value

    def stimulate(self, region: str, amount: float):
        if region in self.regions:
            self.regions[region] += amount