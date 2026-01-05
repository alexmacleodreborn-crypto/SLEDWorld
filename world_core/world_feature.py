# world_core/world_feature.py

class WorldFeature:
    """
    Sub-object inside a place.
    Has a local position relative to the parent place.
    """

    def __init__(
        self,
        name: str,
        local_position: tuple[float, float, float],
        kind: str,
    ):
        self.name = name
        self.local_position = local_position  # (dx, dy, dz)
        self.kind = kind

    def snapshot(self):
        return {
            "name": self.name,
            "kind": self.kind,
            "local_position": self.local_position,
        }