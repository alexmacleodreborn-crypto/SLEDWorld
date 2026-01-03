class MotherBot:
    """
    Persistent maternal sensory source.
    Exists before and after birth.
    """

    def __init__(self):
        self.heartbeat = 0.8
        self.voice = 0.4
        self.motion = 0.3

    def sensory_output(self, *, prebirth: bool):
        if prebirth:
            return {
                "heartbeat": self.heartbeat,
                "pressure": 0.6,
                "sound": 0.4,
                "motion": 0.3
            }
        else:
            return {
                "voice": self.voice,
                "motion": 0.4,
                "sound": 0.5
            }