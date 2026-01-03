from .event_applier import apply_event
from .experience_event import ExperienceEvent

class DayCycle:
    """
    Observer-driven developmental cycle controller.
    """

    def __init__(self, a7do):
        self.a7do = a7do
        self.day = 0
        self.has_birthed = False

    def ensure_birth(self):
        if self.has_birthed:
            return

        birth_event = ExperienceEvent(
            place="hospital",
            channels={
                "pressure": 1.0,
                "sound": 0.9,
                "light": 0.7,
                "motion": 0.8
            },
            intensity=1.0
        )

        apply_event(self.a7do, birth_event)
        self.a7do.mark_birthed()
        self.has_birthed = True

    def wake(self):
        self.a7do.is_awake = True
        self.a7do.log(f"day {self.day}: wake")

    def sleep(self):
        self.a7do.is_awake = False
        replayed = self.a7do.familiarity.replay()
        self.a7do.log("sleep: replay and consolidation")
        for pat in replayed:
            self.a7do.log(f"sleep replay: {pat}")

    def next_day(self):
        self.day += 1
        self.a7do.log(f"day {self.day} begins")