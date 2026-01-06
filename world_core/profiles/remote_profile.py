from world_core.world_object import WorldObject
import math


class RemoteProfile(WorldObject):
    """
    A portable TV remote.

    Rules:
    - Physical world object
    - Can be picked up or left on surfaces
    - Controls ONE bound TV
    - Control only works within physical range
    - No cognition
    - No time
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        tv,                         # 🔑 bound TVProfile
        range_m: float = 5.0,
    ):
        super().__init__(name=name, position=position)

        if tv is None:
            raise ValueError("RemoteProfile requires a TV reference")

        self.tv = tv
        self.range_m = float(range_m)
        self.held_by = None  # agent name or None

    # =================================================
    # Carry mechanics
    # =================================================

    def pick_up(self, agent_name: str):
        self.held_by = agent_name

    def drop(self, position: tuple[float, float, float]):
        self.held_by = None
        self.position = tuple(float(v) for v in position)

    # =================================================
    # Range check (PHYSICAL)
    # =================================================

    def _in_range(self) -> bool:
        rx, ry, rz = self.position
        tx, ty, tz = self.tv.position

        dx = rx - tx
        dy = ry - ty
        dz = rz - tz

        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        return distance <= self.range_m

    # =================================================
    # Physical interactions (delegated to TV)
    # =================================================

    def power_toggle(self) -> bool:
        if not self._in_range():
            return False
        self.tv.power_toggle()
        return True

    def volume_up(self) -> bool:
        if not self._in_range():
            return False
        self.tv.volume_up()
        return True

    def volume_down(self) -> bool:
        if not self._in_range():
            return False
        self.tv.volume_down()
        return True

    # =================================================
    # Observer snapshot
    # =================================================

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "remote",
            "held_by": self.held_by,
            "range_m": self.range_m,
            "controls": self.tv.name,
        })
        return base