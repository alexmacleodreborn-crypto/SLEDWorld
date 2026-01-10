# world_core/profiles/animal_profile.py

from dataclasses import dataclass
from typing import Tuple

@dataclass
class AnimalProfile:
    name: str
    species: str
    color: str
    position_xyz: Tuple[float,float,float]