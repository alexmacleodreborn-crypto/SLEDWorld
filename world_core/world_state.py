import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Bot:
    name: str
    role: str  # "mum", "dad", "nurse", etc.
    x: float = 0.0
    y: float = 0.0


class WorldState:
    """
    Minimal always-running world.
    - Holds a current place label
    - Provides ambient/light/sound levels
    - Holds bots (mum/dad/etc.)
    - Supports distance checks

    This is intentionally simple and safe.
    """

    def __init__(self, seed: int = 7):
        self.rng = random.Random(seed)
        self.t = 0.0
        self.current_place = "hospital"

        # baseline environment signals
        self._ambient = 0.25
        self._light = 0.35
        self._sound = 0.35

        # bots
        self.bots: List[Bot] = [
            Bot(name="Mum", role="mum", x=0.0, y=0.0),
            Bot(name="Dad", role="dad", x=1.2, y=0.2),
            Bot(name="Nurse", role="nurse", x=0.8, y=0.8),
        ]

        # A7DO physical anchor in world frame (very simple marker)
        self.a7do_x = 0.0
        self.a7do_y = 0.0

    def tick(self, dt: float = 0.25):
        """
        Advance world time and gently vary environment.
        """
        self.t += float(dt)

        # gentle drift (world is never perfectly static)
        self._ambient = self._clamp(self._ambient + self.rng.uniform(-0.01, 0.01))
        self._light = self._clamp(self._light + self.rng.uniform(-0.02, 0.02))
        self._sound = self._clamp(self._sound + self.rng.uniform(-0.02, 0.02))

        # small bot motion
        for b in self.bots:
            b.x += self.rng.uniform(-0.05, 0.05)
            b.y += self.rng.uniform(-0.05, 0.05)

    def set_place(self, place: str):
        self.current_place = place

    def get_bot(self, role: str) -> Optional[Bot]:
        role = role.lower().strip()
        for b in self.bots:
            if b.role.lower() == role:
                return b
        return None

    def distance_between_a7do_and(self, bot: Bot) -> float:
        dx = (self.a7do_x - bot.x)
        dy = (self.a7do_y - bot.y)
        return (dx * dx + dy * dy) ** 0.5

    def ambient_level(self) -> float:
        return float(self._ambient)

    def light_level(self) -> float:
        return float(self._light)

    def sound_level(self) -> float:
        return float(self._sound)

    @staticmethod
    def _clamp(x: float) -> float:
        return max(0.0, min(1.0, float(x)))