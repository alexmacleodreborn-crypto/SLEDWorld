class SoundSource:
    def __init__(self, name, position, base_level=0.6):
        self.name = name
        self.position = position
        self.base_level = float(base_level)
        self.active = False

    def set_active(self, active: bool):
        self.active = bool(active)

    def level(self) -> float:
        return round(self.base_level if self.active else 0.0, 3)