from a7do_core.event_applier import apply_event


class DayCycle:
    """
    Controls A7DO's biological-style daily cycle.
    Observer may only trigger transitions.
    """

    def __init__(self, a7do):
        self.a7do = a7do
        self.day = 0
        self.has_birthed = False

    # -------------------------
    # Birth
    # -------------------------

    def ensure_birth(self):
        """
        Trigger the birth experience exactly once.
        Birth immediately unlocks awareness and wakes A7DO.
        """
        if self.has_birthed:
            return

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

        # Apply birth sensory shock
        apply_event(self.a7do, birth_event)

        # Internal transition: awareness begins
        self.a7do.unlock_awareness()
        self.has_birthed = True

        # Biological truth: birth = awake
        self.wake()

    # -------------------------
    # Wake / Sleep
    # -------------------------

    def wake(self):
        """
        Wake A7DO if asleep.
        """
        if not self.a7do.is_awake:
            self.a7do.is_awake = True
            self.a7do.internal_log.append("wake anchor")

    def sleep(self):
        """
        Put A7DO to sleep and trigger replay.
        """
        if self.a7do.is_awake:
            self.a7do.is_awake = False
            replayed = self.a7do.familiarity.replay()
            self.a7do.internal_log.append("sleep: replay and consolidation")
            for pat in replayed:
                self.a7do.internal_log.append(f"  replayed {pat}")

    # -------------------------
    # Day progression
    # -------------------------

    def next_day(self):
        """
        Advance the biological day counter.
        """
        self.day += 1
        self.a7do.internal_log.append(f"day {self.day} begins")