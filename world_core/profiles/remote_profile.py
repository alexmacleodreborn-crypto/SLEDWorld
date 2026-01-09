# world_core/profiles/remote_profile.py

from world_core.world_object import WorldObject


class RemoteProfile(WorldObject):
    """
    Simple remote that controls a bound TV.
    """

    def __init__(self, name: str, position: tuple[float, float, float], tv):
        super().__init__(name=name, position=position)
        self.tv = tv

        x, y, z = position
        self.set_bounds(
            min_xyz=(x - 0.12, y - 0.05, z - 0.02),
            max_xyz=(x + 0.12, y + 0.05, z + 0.02),
        )

    def power_toggle(self) -> bool:
        if self.tv:
            return self.tv.power_toggle()
        return False

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "remote",
            "bound_to": getattr(self.tv, "name", None),
        })
        return base