# world_core/profiles/person_profile.py

from dataclasses import dataclass
from typing import Tuple

@dataclass
class PersonProfile:
    name: str
    age: int
    home_name: str
    position_xyz: Tuple[float,float,float]