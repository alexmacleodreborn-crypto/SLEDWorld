# world_core/profiles/tv_profile.py

from world_core.world_object import WorldObject
from world_core.sound.sound_source import SoundSource


class TVProfile(WorldObject):
    """
    Wall-mounted TV with:
    - power state
    - sound emission when on
    - LED indicator: red when off, green when on
    """

    def __init__(self, name: str, position: tuple[float, float, float]):
        super().__init__(name=name, position=position)

        self.is_on = False

        # Very small physical bounds (wall-mounted panel)
        x, y, z = position
        w, d, h = 1.2, 0.15, 0.7  # meters
        self.set_bounds(
            min_xyz=(x - w / 2, y - d / 2, z - h / 2),
            max_xyz=(x + w / 2, y + d / 2, z + h / 2),
        )

        # Sound source (only active when on)
        self.sound = SoundSource(
            name=f"{name}_sound",
            position=position,
            base_level=0.6,
        )
        self.sound.set_active(False)

    # -------------------------
    # Outputs
    # -------------------------

    def sound_level(self) -> float:
        # If SoundSource supports active state internally
        return 0.6 if self.is_on else 0.0

    def light_level(self) -> dict:
        """
        TV LED indicator light.
        """
        if self.is_on:
            return {"intensity": 0.8, "color": "green"}
        return {"intensity": 0.3, "color": "red"}

    # -------------------------
    # Actions
    # -------------------------

    def power_toggle(self) -> bool:
        self.is_on = not self.is_on
        try:
            self.sound.set_active(self.is_on)
        except Exception:
            pass
        return True

    # -------------------------
    # Snapshot
    # -------------------------

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "tv",
            "is_on": self.is_on,
            "sound_level": self.sound_level(),
            "light": self.light_level(),
        })
        return base