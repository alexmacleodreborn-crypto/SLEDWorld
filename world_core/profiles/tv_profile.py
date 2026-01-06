# world_core/profiles/tv_profile.py

from world_core.world_object import WorldObject


class TVProfile(WorldObject):
    """
    A television as a physical world object.

    - Has state (on/off, volume)
    - Emits sound when on
    - No cognition
    - No time
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        max_volume: int = 100,
    ):
        super().__init__(name=name, position=position)

        self.on = False
        self.volume = 10
        self.max_volume = int(max_volume)

    # -----------------------------------------
    # Physical interactions (called by agents)
    # -----------------------------------------

    def power_toggle(self):
        self.on = not self.on

    def volume_up(self):
        if self.on:
            self.volume = min(self.volume + 5, self.max_volume)

    def volume_down(self):
        if self.on:
            self.volume = max(self.volume - 5, 0)

    # -----------------------------------------
    # Observable outputs
    # -----------------------------------------

    def sound_level(self) -> float:
        """
        Abstract sound pressure level (0.0 – 1.0).
        """
        if not self.on:
            return 0.0
        return self.volume / self.max_volume

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "tv",
            "on": self.on,
            "volume": self.volume,
            "sound_level": round(self.sound_level(), 2),
        })
        return base