from dataclasses import dataclass, field


@dataclass
class GestationBridge:
    """
    Couples world mother physiology into A7DO pre-birth sensory input.
    Runs continuously while world time advances.
    """

    a7do: object
    mother: object
    clock: object

    completed: bool = False
    elapsed_days: float = 0.0

    def tick(self):
        """
        Advance gestation coupling.
        Called every world tick.
        """

        if self.completed:
            return

        # Advance elapsed gestation time
        self.elapsed_days = self.clock.days_elapsed

        # Pull mother physiology snapshot
        mother_snapshot = self.mother.snapshot()

        # --- DEFENSIVE READ ---
        heartbeat = mother_snapshot.get("heartbeat")

        if heartbeat is None:
            # Mother exists but heartbeat not yet initialised
            return

        # --- PRE-BIRTH SENSORY COUPLING ---
        # Muffled, rhythmic, non-symbolic
        sensory_channels = {
            "pressure": 0.6,
            "sound": 0.4,
            "rhythm": heartbeat.get("amplitude", 1.0),
        }

        # Intensity scales with heartbeat amplitude
        intensity = heartbeat.get("amplitude", 1.0) * 0.5

        self.a7do.familiarity.observe(
            place="womb",
            channels=sensory_channels,
            intensity=intensity,
        )

        # --- AUTO BIRTH CONDITION ---
        # Example: 270 days ≈ 9 months
        if self.elapsed_days >= 270:
            self.completed = True
            self.a7do.internal_log.append(
                "gestation complete → birth transition ready"
            )