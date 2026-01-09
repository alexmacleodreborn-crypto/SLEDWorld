# world_core/sound/sound_field.py

import math

class SoundField:
    """
    Physical sound propagation field.
    """

    def __init__(self):
        self.sources = []

    def register(self, source):
        self.sources.append(source)

    def sample(self, x, y, z):
        total = 0.0

        for src in self.sources:
            level = src.get_level()
            if level <= 0:
                continue

            sx, sy, sz = src.position
            dx = x - sx
            dy = y - sy
            dz = z - sz
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)

            if dist < 1.0:
                attenuation = 1.0
            else:
                attenuation = 1.0 / (dist * dist)

            attenuation = max(attenuation, 0.02)
            total += level * attenuation

        return round(min(total, 1.0), 3)