# world_core/sound/sound_source.py

class SoundSource:
    """
    Physical sound emitter.
    No semantics.
    """

    def __init__(self, name, position, base_level=1.0):
        self.name = name
        self.position = position
        self.base_level = base_level
        self.active = False

    def set_active(self, state: bool):
        self.active = state

    def get_level(self):
        if not self.active:
            return 0.0
        return float(self.base_level)