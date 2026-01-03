class BodyState:
    """
    Binary body state only.
    No interpretation here.
    """

    def __init__(self):
        self.is_asleep = True

    def wake(self):
        self.is_asleep = False

    def sleep(self):
        self.is_asleep = True