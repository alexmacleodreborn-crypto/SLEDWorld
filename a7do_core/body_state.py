import random

class BodyState:
    """
    Pre-birth + post-birth biological substrate.
    - Drives: hunger, wetness, fatigue
    - Arousal/comfort as regulation signals
    - Growth: motor strength, sensory gain, reflex rate
    """

    def __init__(self, prebirth: bool = True, seed: int = 7):
        self.rng = random.Random(seed)

        # drives (0..1)
        self.hunger = 0.2
        self.wetness = 0.1
        self.fatigue = 0.2

        # regulation
        self.arousal = 0.2
        self.comfort = 0.1

        # growth & capability
        self.prebirth = prebirth
        self.sensory_gain = 0.15 if prebirth else 0.60   # ramps up prebirth
        self.motor_strength = 0.10 if prebirth else 0.50
        self.reflex_rate = 0.20 if prebirth else 0.40    # chance of reflex/kick each tick
        self.breathing_rhythm = 0.0                      # becomes meaningful at birth

        # internal pain/itch style signals (0..1)
        self.local_irritation = 0.0

    # ─────────────────────────────────────────────
    # Growth + gating
    # ─────────────────────────────────────────────
    def grow_tick(self, dt: float = 1.0):
        """
        Organic growth: very slow prebirth ramp, then stable postbirth adaptation.
        """
        if self.prebirth:
            self.sensory_gain = min(0.55, self.sensory_gain + 0.010 * dt)
            self.motor_strength = min(0.55, self.motor_strength + 0.008 * dt)
            self.reflex_rate = min(0.55, self.reflex_rate + 0.006 * dt)
        else:
            # postbirth: growth slower, stabilizing
            self.sensory_gain = min(1.0, self.sensory_gain + 0.003 * dt)
            self.motor_strength = min(1.0, self.motor_strength + 0.003 * dt)
            self.reflex_rate = min(1.0, self.reflex_rate + 0.0015 * dt)

    def unlock_birth_transition(self):
        """
        Birth unlock: sensory gain jump, motor jump, breathing becomes an active rhythm.
        """
        self.prebirth = False
        self.sensory_gain = max(self.sensory_gain, 0.75)
        self.motor_strength = max(self.motor_strength, 0.65)
        self.reflex_rate = max(self.reflex_rate, 0.45)
        self.breathing_rhythm = 1.0
        self.arousal = min(1.0, self.arousal + 0.4)

    # ─────────────────────────────────────────────
    # Awake/sleep drift (prebirth) and awake/sleep (postbirth)
    # ─────────────────────────────────────────────
    def tick_awake(self, dt: float = 1.0):
        """
        Awake tick: drives increase, discomfort modulates arousal/comfort.
        """
        self.hunger = min(1.0, self.hunger + (0.010 if self.prebirth else 0.03) * dt)
        self.wetness = min(1.0, self.wetness + (0.008 if self.prebirth else 0.02) * dt)
        self.fatigue = min(1.0, self.fatigue + (0.020 if self.prebirth else 0.04) * dt)

        discomfort = 0.0
        if self.hunger > 0.8:
            discomfort += 0.10
        if self.wetness > 0.8:
            discomfort += 0.10
        if self.local_irritation > 0.7:
            discomfort += 0.08

        self.comfort = max(-1.0, self.comfort - discomfort)
        self.arousal = min(2.0, self.arousal + discomfort)

        # small random irritation signals appear (itch/pain precursors)
        if self.rng.random() < (0.03 if self.prebirth else 0.02):
            self.local_irritation = min(1.0, self.local_irritation + 0.15)

        # irritation can naturally fade
        self.local_irritation = max(0.0, self.local_irritation - 0.03 * dt)

    def sleep_tick(self, dt: float = 1.0):
        """
        Sleep tick: fatigue drops, arousal settles, comfort rises.
        """
        self.fatigue = max(0.0, self.fatigue - (0.06 if self.prebirth else 0.10) * dt)
        self.arousal = max(0.0, self.arousal - (0.10 if self.prebirth else 0.20) * dt)
        self.comfort = min(1.0, self.comfort + 0.05 * dt)

        # hunger/wetness drift slowly even during sleep
        self.hunger = min(1.0, self.hunger + 0.005 * dt)
        self.wetness = min(1.0, self.wetness + 0.004 * dt)

    def should_sleep(self) -> bool:
        """
        Prebirth: drifting (fatigue + low arousal).
        Postbirth: clearer threshold.
        """
        if self.prebirth:
            return self.fatigue > 0.65 and self.arousal < 0.9
        return self.fatigue >= 0.75 and self.arousal < 1.5

    # ─────────────────────────────────────────────
    # Event modulation hooks (used by event_applier)
    # ─────────────────────────────────────────────
    def apply_intensity(self, intensity: float):
        """
        Intensity maps into arousal/fatigue, scaled by sensory_gain.
        """
        g = self.sensory_gain
        self.arousal = min(2.0, self.arousal + 0.25 * intensity * g)
        self.fatigue = min(1.0, self.fatigue + 0.10 * intensity * g)

    def apply_channels(self, channels: dict):
        """
        Channels are pre-symbolic: light/noise/pressure/touch/temperature etc.
        We only modulate regulation.
        """
        total = 0.0
        for v in channels.values():
            try:
                total += float(v)
            except Exception:
                pass
        total = max(0.0, min(5.0, total))
        self.arousal = min(2.0, self.arousal + 0.05 * total * self.sensory_gain)

    # ─────────────────────────────────────────────
    # Prebirth motor reflex: kicks/grabs (no intention)
    # ─────────────────────────────────────────────
    def maybe_reflex(self) -> str | None:
        """
        Returns a reflex label occasionally (kick/turn/grasp).
        """
        if self.rng.random() < self.reflex_rate:
            return self.rng.choice(["kick-legs", "curl-fingers", "turn-head", "stretch-arms"])
        return None