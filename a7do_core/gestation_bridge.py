# sledworld/a7do_core/gestation_bridge.py

class GestationBridge:
    """
    Couples mother sensory field to A7DO pre-birth.
    Applies damping + familiarity imprinting.
    """

    def __init__(self, a7do, mother):
        self.a7do = a7do
        self.mother = mother
        self.completed = False
        self.elapsed_days = 0.0

    def tick(self, dt_seconds: float, world_days_elapsed: float):
        if self.completed:
            return

        self.elapsed_days = world_days_elapsed

        # Advance both bodies
        self.a7do.body.tick(dt_seconds)
        mother_signal = self.mother.tick(dt_seconds)

        # Pre-birth familiarity imprint (muted)
        self.a7do.familiarity.observe(
            place="womb",
            channels={
                "heartbeat": mother_signal["heartbeat"],
                "sound": mother_signal["muffled_sound"],
                "pressure": mother_signal["pressure"],
            },
            intensity=0.4,
        )

        # Automatic birth at ~270 days
        if self.elapsed_days >= 270:
            self.completed = True
            self.a7do.internal_log.append(
                "birth transition: sensory shock + separation"
            )
            self.a7do.unlock_awareness()