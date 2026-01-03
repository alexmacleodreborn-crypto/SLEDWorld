# a7do_core/day_cycle.py

from .event_applier import apply_event

GESTATION_LIMIT = 180  # abstracted ~6 months

class DayCycle:
    """
    Controls wake/sleep cycles and birth allowance.
    """

    def __init__(self, a7do):
        self.a7do = a7do
        self.day = 0
        self.has_birthed = False

    # ---------- Pre-birth cycles ----------

    def prebirth_cycle(self):
        if self.has_birthed:
            return

        self.a7do.prebirth_wake()

        # Ambient womb sensory background
        womb_event = {
            "place": "womb",
            "channels": {
                "heartbeat": 0.8,
                "pressure": 0.6,
                "sound": 0.4
            },
            "intensity": 0.3
        }
        apply_event(self.a7do, womb_event)

        self.a7do.prebirth_sleep()

        # Automatic birth allowance
        if self.a7do.gestation_cycles >= GESTATION_LIMIT:
            self.ensure_birth()

    # ---------- Birth ----------

    def ensure_birth(self):
        if self.has_birthed:
            return

        self.has_birthed = True

        birth_event = {
            "place": "womb",
            "channels": {
                "pressure": 1.0,
                "sound": 1.0,
                "motion": 1.0,
                "light": 0.3
            },
            "intensity": 1.0
        }

        apply_event(self.a7do, birth_event)
        self.a7do.unlock_birth()

    # ---------- Post-birth ----------

    def wake(self):
        self.a7do.is_awake = True
        self.a7do.internal_log.append("wake")

    def sleep(self):
        self.a7do.sleep()

    def next_day(self):
        self.day += 1
        self.a7do.internal_log.append(f"day {self.day} begins")