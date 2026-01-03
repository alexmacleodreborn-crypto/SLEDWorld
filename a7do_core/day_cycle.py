from .event_applier import apply_event

class DayCycle:
    """
    Runs continuous prebirth and postbirth windows.
    Prebirth: "womb" place, muted sensory, drift sleep/awake, growth ramps.
    Birth: explicit transition event.
    Postbirth: home/hospital, clearer wake/sleep.
    """

    def __init__(self, a7do, world=None):
        self.a7do = a7do
        self.world = world
        self.awake = False

    def run_prebirth_window(self, n_ticks: int = 30):
        """
        Prebirth continuous sensory baseline + growth + reflex.
        """
        self.a7do.log.add("prebirth: window start")
        for _ in range(n_ticks):
            # growth always runs
            self.a7do.body.grow_tick(dt=1.0)

            # fetal drift awake/sleep
            if not self.awake:
                # sleeping
                self.a7do.body.sleep_tick(dt=1.0)
                if self.a7do.body.fatigue < 0.35:
                    self.awake = True
                    self.a7do.log.add("prebirth: drift awake")
            else:
                # awake-ish
                self.a7do.body.tick_awake(dt=1.0)

                # constant womb noise/pressure baseline
                apply_event(self.a7do, {
                    "type": "experience",
                    "place": "womb",
                    "intensity": 0.35,
                    "channels": {
                        "noise": 0.45,
                        "pressure": 0.35,
                        "warmth": 0.25
                    }
                })

                if self.a7do.body.should_sleep():
                    self.awake = False
                    self.a7do.log.add("prebirth: drift sleep")

        self.a7do.log.add("prebirth: window end")

    def trigger_birth(self):
        """
        World birth event triggers internal transition.
        """
        apply_event(self.a7do, {
            "type": "birth",
            "place": "hospital",
            "intensity": 1.0,
            "channels": {
                "pressure": 1.0,
                "noise": 1.0,
                "light": 1.0,
                "touch": 1.0,
            }
        })

    def run_postbirth_window(self, place: str = "home", n_ticks: int = 20):
        """
        Postbirth continuous feed while awake, auto sleep when fatigue threshold.
        """
        if not self.a7do.birthed:
            self.a7do.log.add("postbirth blocked: not birthed")
            return

        self.a7do.log.add(f"postbirth: window start place={place}")
        self.awake = True

        for _ in range(n_ticks):
            self.a7do.body.grow_tick(dt=1.0)
            self.a7do.body.tick_awake(dt=1.0)

            # ambient baseline
            apply_event(self.a7do, {
                "type": "experience",
                "place": place,
                "intensity": 0.55,
                "channels": {
                    "noise": 0.35,
                    "light": 0.40,
                    "touch": 0.25
                }
            })

            if self.a7do.body.should_sleep():
                self.awake = False
                self.a7do.log.add("sleep onset (body-induced)")
                break

        self.a7do.log.add("postbirth: window end")

    def sleep_and_consolidate(self):
        """
        Sleep replay reinforces familiar patterns.
        """
        replayed = self.a7do.familiarity.replay(n=5)
        self.a7do.log.add("sleep: replay and consolidation")
        for pat in replayed:
            self.a7do.log.add(f"sleep-replay: {pat}")

        # run a few sleep ticks to settle body
        for _ in range(8):
            self.a7do.body.sleep_tick(dt=1.0)

        self.a7do.next_day()