from world_core.sound.sound_source import SoundSource
from world_core.light.light_source import LightSource


class TVProfile:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.is_on = False

        self.sound = SoundSource(
            name=f"{name}_sound",
            position=position,
            base_level=0.6,
        )

        self.light = LightSource(
            name=f"{name}_light",
            position=position,
            base_level=1.0,
        )

    def power_toggle(self):
        self.is_on = not self.is_on
        self.sound.set_active(self.is_on)
        self.light.set_active(self.is_on)