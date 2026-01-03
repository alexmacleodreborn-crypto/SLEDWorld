class GestationBridge:
    """
    Couples mother physiology into A7DO physiology.
    This is pre-birth ONLY.
    """

    def __init__(self, mother, a7do):
        self.mother = mother
        self.a7do = a7do
        self.completed = False

    def tick(self, dt: float):
        if self.completed:
            return

        # 1. Heartbeat entrainment (bias, not sync)
        delta = (
            self.mother.heartbeat_phase
            - self.a7do.phys.heartbeat_phase
        )
        self.a7do.phys.heartbeat_phase += delta * 0.02

        # 2. Pressure modulation
        stress_factor = 1.0 + self.mother.stress
        self.a7do.phys.pressure += dt * 0.01 * stress_factor

        # 3. Activity adds background arousal
        self.a7do.phys.arousal += dt * self.mother.activity * 0.01

    def end_gestation(self):
        self.completed = True