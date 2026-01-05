# world_core/world_object.py

class WorldObject:
    """
    Base class for all objective world entities.
    Pure data. No agents. No cognition.
    """

    def __init__(self, name: str, position: tuple[float, float, float]):
        if (
            not isinstance(position, tuple)
            or len(position) != 3
        ):
            raise ValueError(
                f"WorldObject '{name}' requires position=(x, y, z)"
            )

        x, y, z = position

        # Enforce numeric coordinates
        try:
            self.position = (float(x), float(y), float(z))
        except Exception:
            raise ValueError(
                f"Invalid position values for '{name}': {position}"
            )

        self.name = name

    # -----------------------------------------
    # Observer snapshot
    # -----------------------------------------

    def snapshot(self):
        return {
            "name": self.name,
            "position": {
                "x": self.position[0],
                "y": self.position[1],
                "z": self.position[2],
            },
        }