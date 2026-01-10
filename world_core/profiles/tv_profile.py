import math
from world_core.sound.sound_source import SoundSource
from world_core.light.light_source import LightSource

class TVProfile:
    def __init__(self, name, position):
        self.name = name
        self.position = tuple(position)
        self.is_on = False

        self.sound = SoundSource(name=f"{name}:sound", position=position, base_level=0.6)
        self.light = LightSource(name=f"{name}:light", position=position, base_level=0.8)

        # off state shows red LED
        self.light.set_active(True, color="red")
        self.sound.set_active(False)

    def power_toggle(self):
        self.is_on = not self.is_on
        self.sound.set_active(self.is_on)
        # On => green; Off => red (still emitting a small light)
        if self.is_on:
            self.light.set_active(True, color="green")
        else:
            self.light.set_active(True, color="red")

    def _attenuate(self, p_xyz, base):
        x, y, z = p_xyz
        ox, oy, oz = self.position
        dx, dy, dz = x-ox, y-oy, z-oz
        d = math.sqrt(dx*dx + dy*dy + dz*dz)
        if d < 1.0:
            return base
        return base / (d*d)

    def sound_level_at(self, p_xyz):
        base = self.sound.level()
        return min(1.0, self._attenuate(p_xyz, base))

    def light_level_at(self, p_xyz):
        base = self.light.level()
        return min(1.0, self._attenuate(p_xyz, base))

    def snapshot(self):
        return {
            "type": "tv",
            "name": self.name,
            "position": self.position,
            "is_on": self.is_on,
            "sound_level": self.sound.level(),
            "light_level": self.light.level(),
            "light_color": self.light.color,
        }