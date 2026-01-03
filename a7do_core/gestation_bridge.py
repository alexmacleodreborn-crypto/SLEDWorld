# a7do_core/gestation_bridge.py

class GestationBridge:
    """
    Bridges always-on world time into pre-birth A7DO experience.
    Handles automatic transition to birth.
    """

    GESTATION_DAYS = 180.0  # ~6 months compressed

    def __init__(self, a7do, world_clock):
        self.a7do = a7do
        self.clock = world_clock
        self.last_sample_minute = 0.0

    def tick(self):
        """
        Called every world tick.
        """

        # Update elapsed gestation time
        elapsed = self.clock.days_elapsed

        # Pre-birth sensory exposure
        if not self.a7do.birthed:
            self._prebirth_experience(elapsed)

            if elapsed >= self.GESTATION_DAYS:
                self._trigger_birth()

    def _prebirth_experience(self, elapsed_days: float):
        """
        Very low-level, gated sensory imprinting.
        """

        # Sample roughly every 30 world minutes
        if self.clock.minutes - self.last_sample_minute < 30:
            return

        self.last_sample_minute = self.clock.minutes

        # Pre-birth muted sensory exposure
        self.a7do.familiarity.observe(
            place="womb",
            channels={
                "heartbeat": 0.6,
                "pressure": 0.4,
                "muffled_sound": 0.3,
            },
            intensity=0.5,
        )

        self.a7do.internal_log.append(
            "prebirth: rhythmic sensory exposure"
        )

    def _trigger_birth(self):
        """
        Automatic birth transition.
        """
        self.a7do.mark_birthed()
        self.a7do.familiarity.unlock()

        self.a7do.internal_log.append(
            "birth: awareness gate opened"
        )