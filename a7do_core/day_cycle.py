from .event_applier import apply_event

class DayCycle:
    """
    Regulates wake / sleep and birth sequencing.
    """

    def __init__(self, a7do):
        self.a7do = a7do
        self.has_birthed = False
        self.day = 0
        self._last_replay = []

    def ensure_birth(self):
        if self.has_birthed:
            return

        birth_event = {
            "place": "hospital",
            "channels": {
                "pressure": 1.0,
                "sound": 0.9,
                "light": 0.8,
                "motion": 0.9,
            },
            "intensity": 1.0,
        }

        apply_event(self.a7do, birth_event)
        self.a7do.mark_birthed()
        self.has_birthed = True

    def wake(self):
        self.a7do.wake()

    def sleep(self):
        self.a7do.sleep()
        self._last_replay = self.a7do.familiarity.replay()

    def next_day(self):
        self.day += 1

    # ---------- Observer hook ----------

    def last_sleep_replay(self):
        return self._last_replay