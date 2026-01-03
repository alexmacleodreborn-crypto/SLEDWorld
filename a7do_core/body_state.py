class BodyState:
    """
    Pre-symbolic body regulation for newborn routine.
    No language. No concepts. Only internal state + intensity.
    """

    def __init__(self):
        # 0..1 scaled internal drives
        self.hunger = 0.4
        self.wetness = 0.1
        self.fatigue = 0.2

        # meta
        self.arousal = 0.0
        self.comfort = 0.0

        # last actions (for replay cues)
        self.last_feed_tick = None
        self.last_change_tick = None

    def tick_awake(self, dt: float = 1.0):
        """
        dt is an abstract step. We keep it simple.
        Awake tick increases hunger, wetness, fatigue.
        """
        self.hunger = min(1.0, self.hunger + 0.03 * dt)
        self.wetness = min(1.0, self.wetness + 0.02 * dt)
        self.fatigue = min(1.0, self.fatigue + 0.04 * dt)

        # internal discomfort grows if hungry or wet
        discomfort = 0.0
        if self.hunger > 0.7:
            discomfort += 0.15
        if self.wetness > 0.7:
            discomfort += 0.15

        self.comfort -= discomfort
        self.arousal += discomfort

    def feed(self, tick_index: int):
        self.hunger = max(0.0, self.hunger - 0.6)
        self.comfort += 0.25
        self.arousal = max(0.0, self.arousal - 0.15)
        self.last_feed_tick = tick_index

    def change(self, tick_index: int):
        self.wetness = max(0.0, self.wetness - 0.8)
        self.comfort += 0.20
        self.arousal = max(0.0, self.arousal - 0.10)
        self.last_change_tick = tick_index

    def soothe(self):
        self.comfort += 0.10
        self.arousal = max(0.0, self.arousal - 0.08)

    def can_sleep(self) -> bool:
        """
        Body-induced sleep:
        - fatigue high enough
        - and arousal not spiking too hard
        """
        return self.fatigue >= 0.75 and self.arousal < 1.5

    def sleep_tick(self, dt: float = 1.0):
        """
        During sleep: fatigue reduces, arousal settles,
        hunger rises slowly, wetness rises slowly.
        """
        self.fatigue = max(0.0, self.fatigue - 0.10 * dt)
        self.arousal = max(0.0, self.arousal - 0.20 * dt)
        self.comfort += 0.05

        self.hunger = min(1.0, self.hunger + 0.01 * dt)
        self.wetness = min(1.0, self.wetness + 0.01 * dt)