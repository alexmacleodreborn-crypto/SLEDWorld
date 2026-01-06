from world_core.world_object import WorldObject


class TVProfile(WorldObject):
    """
    A television as a physical world object.

    Rules:
    - Pure world-layer object
    - Has physical volume in WORLD space
    - Has state (on/off, volume)
    - Emits sound when on
    - No cognition
    - No internal time
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        size: tuple[float, float, float] = (1.2, 0.3, 0.8),  # width, depth, height (meters)
        max_volume: int = 100,
    ):
        super().__init__(name=name, position=position)

        width, depth, height = size
        x, y, z = position

        # -----------------------------------------
        # World-space bounding box (AUTHORITATIVE)
        # -----------------------------------------
        self.set_bounds(
            min_xyz=(x, y, z),
            max_xyz=(x + width, y + depth, z + height),
        )

        # -----------------------------------------
        # Physical properties
        # -----------------------------------------
        self.size = {
            "width": float(width),
            "depth": float(depth),
            "height": float(height),
        }

        # -----------------------------------------
        # Device state
        # -----------------------------------------
        self.on = False
        self.volume = 10
        self.max_volume = int(max_volume)

        # Canonical semantic label (observer-only)
        self.label = "object:tv"

    # =================================================
    # Physical interactions (called by agents)
    # =================================================

    def power_toggle(self):
        self.on = not self.on

    def volume_up(self):
        if self.on:
            self.volume = min(self.volume + 5, self.max_volume)

    def volume_down(self):
        if self.on:
            self.volume = max(self.volume - 5, 0)

    # =================================================
    # Observable outputs
    # =================================================

    def sound_level(self) -> float:
        """
        Abstract sound pressure level (0.0 – 1.0).
        """
        if not self.on:
            return 0.0
        return self.volume / self.max_volume

    # =================================================
    # Observer snapshot
    # =================================================

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "tv",
            "label": self.label,
            "on": self.on,
            "volume": self.volume,
            "max_volume": self.max_volume,
            "sound_level": round(self.sound_level(), 2),
            "size": self.size,
        })
        return base