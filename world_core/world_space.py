# world_core/world_space.py

from typing import Dict, Tuple
from world_core.region import Region

class WorldSpace:
    """
    Absolute 3D physical space.
    No agents. No time. No perception.
    """

    def __init__(self, size=(10_000, 10_000, 10_000), region_size=100):
        self.size = size
        self.region_size = region_size
        self.regions: Dict[Tuple[int, int, int], Region] = {}

    def region_key(self, x, y, z):
        return (
            int(x // self.region_size),
            int(y // self.region_size),
            int(z // self.region_size),
        )

    def get_region(self, x, y, z):
        key = self.region_key(x, y, z)
        if key not in self.regions:
            self.regions[key] = Region(key)
        return self.regions[key]

    def add_object(self, obj):
        region = self.get_region(*obj.position)
        region.add_object(obj)