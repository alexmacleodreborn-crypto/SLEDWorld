from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Place:
    name: str
    kind: str  # hospital, home, park, street
    ambient_noise: str
    smells: List[str]
    light_level: float

@dataclass
class WorldState:
    day: int = 0
    time_of_day: float = 0.0  # 0–24
    places: Dict[str, Place] = field(default_factory=dict)
    bots: Dict[str, "Bot"] = field(default_factory=dict)
    weather: str = "clear"

    def tick(self, hours: float):
        self.time_of_day += hours
        if self.time_of_day >= 24:
            self.time_of_day -= 24
            self.day += 1