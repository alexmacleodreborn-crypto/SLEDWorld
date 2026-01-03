from dataclasses import dataclass
from typing import Dict

@dataclass
class ExperienceEvent:
    source: str
    payload: Dict
    intensity: float