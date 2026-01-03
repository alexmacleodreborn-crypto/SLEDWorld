# a7do_core/day_cycle.py

from .event_applier import apply_event

class DayCycle:
    """
    Manages wake/sleep and the birth transition.
    """

    def __init__(self, a7do):
        self.a7do = a7do
        self.day = 0
        self.has_birthed = False

    def ensure_birth(self):
        if self.has_birthed:
            return

        self.has_birthed = True

        # Pre-birth sensory surge
        birth_event = {
            "place": "womb",
            "channels": {
                "pressure": 1.0,
                "sound": 0.9,
                "motion": 1.0,
                "light": 0.2
            },
            "intensity": 1.0
        }

        apply_event(self.a7do, birth_event)
        self.a7do.unlock_birth()

    def wake(self):
        self.a7do.wake()

    def sleep(self):
        self.a7do.sleep()

    def next_day(self):
        self.day += 1
        self.a7do.internal_log.append(f"day {self.day} begins")