from .event_applier import apply_event
from .sleep import sleep_consolidate

class DayCycle:
    """
    Observer controls *starting* wake and running a window.
    Sleep is body-induced when fatigue threshold is reached.
    """

    def __init__(self, a7do, world):
        self.a7do = a7do
        self.world = world

        self.current_place = None
        self.awake = False
        self.tick_index = 0

    def ensure_birth(self):
        if self.a7do.birthed:
            return

        self.a7do.mark_birthed()
        self.current_place = self.world.birth_place
        self.awake = True
        self.a7do.perceived.update_place(self.current_place)

        for ev in self.world.birth_events():
            apply_event(self.a7do, ev)

        # After birth anchor, we allow a gentle move to home later via observer action
        self.a7do.log.add("birth-anchor complete")

    def wake(self):
        if not self.a7do.birthed:
            self.a7do.log.add("wake blocked: not birthed")
            return
        self.awake = True
        if self.current_place is None:
            self.current_place = self.world.home_place
        self.a7do.perceived.update_place(self.current_place)
        self.a7do.log.add("wake anchor")

    def _body_snapshot(self):
        return {
            "hunger": self.a7do.body.hunger,
            "wetness": self.a7do.body.wetness,
            "fatigue": self.a7do.body.fatigue,
        }

    def run_day_window(self, n_ticks: int = 20):
        """
        This is your '30 seconds' equivalent block.
        Each tick emits low-information sensory events.
        Care actions happen based on body state.
        """
        if not self.a7do.birthed:
            self.a7do.log.add("run blocked: not birthed")
            return

        if not self.awake:
            self.a7do.log.add("run blocked: currently asleep")
            return

        if self.current_place is None:
            self.current_place = self.world.home_place

        for _ in range(n_ticks):
            self.tick_index += 1

            # Body evolves while awake
            self.a7do.body.tick_awake(dt=1.0)

            # Caregiver routine triggers (still pre-language)
            if self.a7do.body.hunger > 0.85:
                self.a7do.body.feed(self.tick_index)
                apply_event(self.a7do, {
                    "place": self.current_place,
                    "intensity": 1.2,
                    "pattern": "care-feeding-warmth"
                })
                self.a7do.log.add("care: feeding applied")

            if self.a7do.body.wetness > 0.85:
                self.a7do.body.change(self.tick_index)
                apply_event(self.a7do, {
                    "place": self.current_place,
                    "intensity": 1.2,
                    "pattern": "care-changing-clean"
                })
                self.a7do.log.add("care: changing applied")

            # Continuous sensory stream from world
            events = self.world.newborn_tick_events(
                place=self.current_place,
                tick_index=self.tick_index,
                body_snapshot=self._body_snapshot()
            )
            for ev in events:
                apply_event(self.a7do, ev)

            # Body-induced sleep
            if self.a7do.body.can_sleep():
                self.awake = False
                self.a7do.log.add("sleep onset (body-induced)")
                break

    def sleep_and_advance(self):
        """
        Observer can force the sleep phase to run + advance day.
        """
        sleep_consolidate(self.a7do)
        self.awake = False
        self.a7do.next_day()
        self.world.day += 1
        # New day starts at home by default after birth era
        self.current_place = self.world.home_place
        self.a7do.perceived.update_place(self.current_place)