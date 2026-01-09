from world_core.sound.sound_source import SoundSource

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

    def power_toggle(self):
        self.is_on = not self.is_on
        self.sound.set_active(self.is_on)
        return True

    # 🔑 REQUIRED
    def light_signal(self):
        return {
            "intensity": 0.9 if self.is_on else 0.2,
            "color": "green" if self.is_on else "red",
        }

    def sound_level(self):
        return self.sound.level if self.is_on else 0.0

    def snapshot(self):
        return {
            "type": "tv",
            "name": self.name,
            "position": self.position,
            "is_on": self.is_on,
            "signals": {
                "sound": self.sound_level(),
                "light": self.light_signal(),
            }
        }