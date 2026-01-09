# world_core/profiles/tv_profile.py

from world_core.sound.sound_source import SoundSource


class TVProfile:
    """
    TV is a world object-like profile with state and signals.
    Emits:
      - sound (0..1)
      - light intensity (0..1) and color ("red"/"green")
    """

    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.is_on = False

        # Sound source is authoritative for "TV noise"
        self.sound = SoundSource(
            name=f"{name}_sound",
            position=position,
            base_level=0.6,
        )
        self.sound.set_active(False)

    def power_toggle(self):
        self.is_on = not self.is_on
        self.sound.set_active(self.is_on)
        return True

    def sound_level(self) -> float:
        # If SoundSource exposes .level use it; otherwise fallback to base_level when active.
        if not self.is_on:
            return 0.0
        lvl = getattr(self.sound, "level", None)
        if isinstance(lvl, (int, float)):
            return float(lvl)
        return float(getattr(self.sound, "base_level", 0.6))

    def light_signal(self) -> dict:
        # Red standby LED when off; green when on
        return {
            "intensity": 0.2 if not self.is_on else 0.9,
            "color": "red" if not self.is_on else "green",
        }

    def snapshot(self):
        return {
            "type": "tv",
            "name": self.name,
            "position": self.position,
            "is_on": self.is_on,
            "signals": {
                "sound": round(self.sound_level(), 3),
                "light": self.light_signal(),
            },
        }