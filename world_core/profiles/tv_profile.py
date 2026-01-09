# world_core/profiles/tv_profile.py

from world_core.sound.sound_source import SoundSource


class TVProfile:
    """
    Physical device.
    - Binary state
    - Sound when ON
    - Light ALWAYS (red when OFF, green when ON)
    - No semantics required by bots
    """

    def __init__(self, name, position):
        self.name = name
        self.position = position

        self.is_on = False

        self.sound = SoundSource(
            name=f"{name}_sound",
            position=position,
            base_level=0.6,
        )

        # Light sensor output always present
        self.light_intensity = 0.8

        # Optional: a human-assigned symbol exists ONLY on the object
        # Bots do not have to use this until evidence binds it.
        self.symbol_hint = "TV"

        # Ensure OFF state is silent
        if hasattr(self.sound, "set_active"):
            self.sound.set_active(False)

    def power_toggle(self):
        self.is_on = not self.is_on
        if hasattr(self.sound, "set_active"):
            self.sound.set_active(self.is_on)
        return True

    def get_sound_level(self) -> float:
        # Support multiple SoundSource implementations safely
        if hasattr(self.sound, "current_level"):
            try:
                return float(self.sound.current_level())
            except Exception:
                return 0.0
        if hasattr(self.sound, "level"):
            try:
                return float(self.sound.level)
            except Exception:
                return 0.0
        # If we can’t read, infer
        return 0.6 if self.is_on else 0.0

    def get_light_output(self) -> dict:
        return {
            "intensity": float(self.light_intensity),
            "color": "green" if self.is_on else "red",
        }

    def snapshot(self):
        return {
            "type": "device",
            "device_kind": "screen_emitter",
            "name": self.name,
            "position": self.position,
            "is_on": bool(self.is_on),
            "sound_level": round(self.get_sound_level(), 3),
            "light": self.get_light_output(),
            # hint exists but should be ignored by most bots until bound
            "symbol_hint": self.symbol_hint,
        }