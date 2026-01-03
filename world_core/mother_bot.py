from dataclasses import dataclass, field
import random


@dataclass
class MotherBot:
    """
    Primary caregiver bot.
    Exists before birth and after birth.
    Provides continuous sensory substrate, not explicit teaching.
    """

    name: str = "Mother"
    heart_rate: float = 72.0
    stress_level: float = 0.2
    activity_level: float = 0.3  # walking, sitting, lying
    voice_presence: float = 0.1  # muffled pre-birth
    warmth: float = 0.8

    rng: random.Random = field(default_factory=lambda: random.Random(42))

    # Internal counters (world-time driven)
    minutes_since_last_move: int = 0
    minutes_since_last_voice: int = 0

    # -------------------------
    # Pre-birth sensory feed
    # -------------------------

    def prebirth_sensory_snapshot(self) -> dict:
        """
        Sensory information perceived by A7DO while in womb.
        Highly filtered and rhythmic.
        """
        # Small natural variation
        hr = self.heart_rate + self.rng.uniform(-2.0, 2.0)

        movement = self.activity_level + self.rng.uniform(-0.05, 0.05)
        movement = max(0.0, min(1.0, movement))

        voice = 0.0
        if self.minutes_since_last_voice > self.rng.randint(15, 45):
            voice = self.voice_presence + self.rng.uniform(0.0, 0.1)
            self.minutes_since_last_voice = 0
        else:
            self.minutes_since_last_voice += 1

        return {
            "place": "womb",
            "channels": {
                "heartbeat": hr / 100.0,
                "movement": movement,
                "voice": voice,
                "warmth": self.warmth,
            },
            "intensity": 0.4 + movement * 0.2,
        }

    # -------------------------
    # Post-birth caregiving
    # -------------------------

    def postbirth_sensory_snapshot(self, *, holding: bool, feeding: bool) -> dict:
        """
        Sensory feed after birth.
        Still not language, but clearer signals.
        """
        base_intensity = 0.6

        touch = 0.0
        if holding:
            touch = 0.7 + self.rng.uniform(0.0, 0.2)

        voice = 0.0
        if feeding or self.rng.random() < 0.1:
            voice = 0.4 + self.rng.uniform(0.0, 0.3)

        return {
            "place": "hospital" if feeding else "home",
            "channels": {
                "heartbeat": self.heart_rate / 100.0,
                "touch": touch,
                "voice": voice,
                "warmth": self.warmth,
            },
            "intensity": base_intensity + touch * 0.3,
        }

    # -------------------------
    # World-time tick
    # -------------------------

    def tick(self, minutes: int = 1):
        """
        Advance mother's internal state with world time.
        """
        self.minutes_since_last_move += minutes
        self.minutes_since_last_voice += minutes

        # Occasionally change activity
        if self.rng.random() < 0.05:
            self.activity_level = self.rng.uniform(0.1, 0.6)

        # Stress fluctuates slowly
        self.stress_level += self.rng.uniform(-0.01, 0.01)
        self.stress_level = max(0.0, min(1.0, self.stress_level))