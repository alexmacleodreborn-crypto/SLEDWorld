class SoundSource:
    """
    Pure physical sound emitter.

    - No cognition
    - No intent
    - Emits energy only
    """

    def __init__(self, name, position, base_volume):
        self.name = name
        self.position = position  # (x, y, z)
        self.base_volume = float(base_volume)  # arbitrary units
        self.active = False

    def turn_on(self):
        self.active = True

    def turn_off(self):
        self.active = False

    def set_volume(self, volume):
        self.base_volume = max(0.0, float(volume))

    def snapshot(self):
        return {
            "name": self.name,
            "active": self.active,
            "base_volume": self.base_volume,
            "position": self.position,
        }