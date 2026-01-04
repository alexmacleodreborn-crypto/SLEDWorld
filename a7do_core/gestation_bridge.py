class GestationBridge:
    """
    Couples mother world signals into A7DO prebirth experience.
    """

    def __init__(self, a7do, mother, clock):
        self.a7do = a7do
        self.mother = mother
        self.clock = clock

        self.elapsed_days = 0
        self.completed = False
        self.phase = "gestation"

    def tick(self):
        if self.completed:
            return

        self.elapsed_days = int(self.clock.total_minutes // (24 * 60))

        signals = self.mother.sensory_snapshot()

        # Convert maternal signals into gated familiarity
        self.a7do.familiarity.observe(
            place="womb",
            channels=signals,
            intensity=0.2,
        )

        # Advance internal body (heartbeat etc)
        self.a7do.body.tick()

        if self.elapsed_days >= 180:
            self.completed = True
            self.phase = "birth_ready"
            self.a7do.unlock_awareness()