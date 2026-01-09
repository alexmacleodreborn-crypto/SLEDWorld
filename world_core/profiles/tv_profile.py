# world_core/profiles/tv_profile.py

from __future__ import annotations
from world_core.sound.sound_source import SoundSource
from world_core.light.light_source import LightSource

class TVProfile:
    """
    Stateful emitter.
    - OFF: red standby light, no sound
    - ON: green light, sound on
    """
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.is_on = False

        self.sound = SoundSource(name=f"{name}:sound", position=position, base_level=0.6)
        self.light = LightSource(name=f"{name}:light", position=position, base_level=0.8)

        # start OFF: red
        self.sound.set_active(False)
        self.light.set_active(True, color="red")

    def power_toggle(self):
        self.is_on = not self.is_on
        if self.is_on:
            self.sound.set_active(True)
            self.light.set_active(True, color="green")
        else:
            self.sound.set_active(False)
            self.light.set_active(True, color="red")
        return True

    def sound_level(self):
        return self.sound.level()

    def light_level(self):
        return self.light.level()

    def snapshot(self):
        return {
            "name": self.name,
            "type": "tv",
            "position": self.position,
            "is_on": self.is_on,
            "sound_level": self.sound.level(),
            "light_level": self.light.level(),
            "light_color": self.light.color,
        }