from __future__ import annotations

class LightSource:
    def __init__(self, name, position, base_level=0.8):
        self.name = name
        self.position = tuple(position)
        self.base_level = float(base_level)
        self.active = False
        self.color = "red"

    def set_active(self, active: bool, color: str = "red"):
        self.active = bool(active)
        self.color = str(color)

    def level(self) -> float:
        return round(self.base_level if self.active else 0.1, 3)  # standby glow