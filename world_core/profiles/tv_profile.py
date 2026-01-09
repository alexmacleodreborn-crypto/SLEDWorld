from world_core.sound.sound_source import SoundSource


class TVProfile:
    """
    Physical TV-like device.

    - Binary state
    - Emits sound when ON
    - Emits light ALWAYS (red/off, green/on)
    - No semantics
    """

    def __init__(self, name, position):
        self.name = name
        self.position = position

        # Physical state
        self.is_on = False

        # Sound emitter
        self.sound = SoundSource(
            name=f"{name}_sound",
            position=position,
            base_level=0.6,
        )

        # Light emitter (always on, colour encodes state)
        self.light_level = 0.8

    # -------------------------
    # Interaction
    # -------------------------

    def power_toggle(self):
        self.is_on = not self.is_on
        self.sound.set_active(self.is_on)

    # -------------------------
    # Field outputs
    # -------------------------

    def get_sound_level(self) -> float:
        return self.sound.current_level()

    def get_light_output(self) -> dict:
        """
        Light is ALWAYS emitted.
        Colour encodes state.
        """
        return {
            "intensity": self.light_level,
            "color": "green" if self.is_on else "red",
        }

    # -------------------------
    # Observer snapshot
    # -------------------------

    def snapshot(self):
        return {
            "type": "device",
            "name": self.name,
            "position": self.position,
            "state": "on" if self.is_on else "off",
            "sound_level": self.get_sound_level(),
            "light": self.get_light_output(),
        }