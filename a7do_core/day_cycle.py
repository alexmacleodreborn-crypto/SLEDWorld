from .event_applier import apply_event
from .sleep import sleep_consolidate

class DayCycle:
    def __init__(self, a7do, world):
        self.a7do = a7do
        self.world = world

    def ensure_birth(self):
        if not self.a7do.birthed:
            self.a7do.mark_birthed()
            for ev in self.world.birth_events():
                apply_event(self.a7do, ev)

    def wake(self):
        self.a7do.log.add("wake anchor")

    def run_day_window(self):
        for ev in self.world.generate_events():
            apply_event(self.a7do, ev)

    def sleep_and_advance(self):
        sleep_consolidate(self.a7do)
        self.a7do.next_day()