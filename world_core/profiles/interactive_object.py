from world_core.world_object import WorldObject


class InteractiveObject(WorldObject):
    """
    Physical interactive object in the world.

    - Has state
    - Has effects (sound/light/etc)
    - No cognition
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        size: tuple[float, float, float],
    ):
        super().__init__(name=name, position=position)

        x, y, z = position
        w, d, h = size

        self.set_bounds(
            min_xyz=(x, y, z),
            max_xyz=(x + w, y + d, z + h),
        )

        self.size = {
            "width": float(w),
            "depth": float(d),
            "height": float(h),
        }

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "size": self.size,
        })
        return base