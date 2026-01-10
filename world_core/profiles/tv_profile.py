from world_core.sound.sound_source import SoundSource
from world_core.light.light_source import LightSource


class TVProfile:
    """
    Physical object:
    - sound output when ON
    - light output always (red standby OFF, green ON)
    """
    def __init__(self, name, position):
        self.name = name
        self.position = tuple(position)
        self.is_on = False

        self.sound = SoundSource(name=f"{name}_sound", position=position, base_level=0.6)
        self.light = LightSource(name=f"{name}_light", position=position, base_level=0.8)

        # standby state
        self.light.set_active(True, color="red")
        self.sound.set_active(False)

    def power_toggle(self):
        self.is_on = not self.is_on
        self.sound.set_active(self.is_on)
        self.light.set_active(True, color=("green" if self.is_on else "red"))
        return True

    def sound_level(self) -> float:
        return self.sound.level()

    def light_level(self) -> float:
        return self.light.level()

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