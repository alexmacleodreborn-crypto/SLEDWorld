class GestationBridge:
    """
    Couples world time, mother, and A7DO pre-birth.
    """

    def __init__(self, a7do, mother, clock, gestation_days=180):
        self.a7do = a7do
        self.mother = mother
        self.clock = clock
        self.gestation_days = gestation_days
        self.completed = False

    def tick(self):
        if self.completed:
            return

        progress = self.clock.days_elapsed / self.gestation_days

        mother_signal = self.mother.snapshot(self.clock.world_minutes)

        self.a7do.familiarity.observe(
            place="womb",
            channels={
                "heartbeat": mother_signal["heartbeat"],
                "pressure": 0.4,
                "sound": 0.2,
            },
            intensity=progress
        )

        self.a7do.body.apply_intensity(progress)

        if progress >= 1.0:
            self.completed = True
            self.a7do.unlock_awareness()
            self.a7do.mark_birthed()