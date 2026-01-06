from world_core.world_object import WorldObject


class RemoteProfile(WorldObject):
    """
    A portable TV remote.

    - Can be picked up
    - Can control a TV if within range
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        range_m: float = 5.0,
    ):
        super().__init__(name=name, position=position)

        self.range_m = float(range_m)
        self.held_by = None  # agent name or None

    # -----------------------------------------
    # Carry mechanics
    # -----------------------------------------

    def pick_up(self, agent_name: str):
        self.held_by = agent_name

    def drop(self, position: tuple[float, float, float]):
        self.held_by = None
        self.position = position

    # -----------------------------------------
    # Observer snapshot
    # -----------------------------------------

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "remote",
            "held_by": self.held_by,
            "range_m": self.range_m,
        })
        return base