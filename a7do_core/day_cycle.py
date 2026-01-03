# a7do_core/day_cycle.py

from a7do_core.event_applier import apply_event

class DayCycle:
    """
    Controls A7DO subjective awareness cycles.
    World time is handled elsewhere.
    """

    def __init__(self, a7do):
        self.a7do = a7do
        self.day_index = 0
        self.has_birthed = False

    def ensure_birth(self):
        if self.has_birthed:
            return

        # Pre-birth ends, birth event occurs
        birth_event = {
            "type": "birth",
            "place": "hospital",
            "intensity": 1.0,
            "channels": {
                "pressure": 1.0,
                "light": 1.0,
                "sound": 1.0,
            },
        }

        apply_event(self.a7do, birth_event)

        self.a7do.unlock_awareness()
        self.has_birthed = True

    def wake(self):
        self.a7do.is_awake = True
        self.a7do.log("wake anchor")

    def sleep(self):
        self.a7do.is_awake = False
        replayed = self.a7do.familiarity.replay()
        self.a7do.log("sleep: replay and consolidation")
        return replayed

    def next_day(self):
        self.day_index += 1
        self.a7do.log(f"day {self.day_index} begins")