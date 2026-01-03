class DayCycle:
    """
    External orchestrator.
    Does NOT own time.
    """

    def __init__(self, a7do):
        self.a7do = a7do
        self.has_birthed = False

    def ensure_birth(self):
        if not self.has_birthed:
            self.a7do.mark_birthed()
            self.has_birthed = True

    def tick(self, dt: float):
        self.a7do.tick(dt)

    def wake(self):
        self.a7do.wake()

    def sleep(self):
        self.a7do.sleep()