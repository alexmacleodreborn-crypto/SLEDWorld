# world_core/world_object.py

class WorldObject:
    """
    Base class for all objective world entities.

    Rules:
    - Pure data
    - No agents
    - No cognition
    - No time
    - Position is an absolute WORLD anchor (x, y, z)
    """

    def __init__(self, name: str, position: tuple[float, float, float]):
        if not isinstance(position, tuple) or len(position) != 3:
            raise ValueError(
                f"WorldObject '{name}' requires position=(x, y, z)"
            )

        try:
            x, y, z = float(position[0]), float(position[1]), float(position[2])
        except Exception:
            raise ValueError(
                f"Invalid position values for '{name}': {position}"
            )

        self.name = str(name)
        self.position = (x, y, z)

        # Optional spatial extent (WORLD-SPACE bounding box)
        # ((min_x, min_y, min_z), (max_x, max_y, max_z))
        self.bounds = None

    # -----------------------------------------
    # Spatial helpers (SAFE, OPTIONAL)
    # -----------------------------------------

    def set_bounds(
        self,
        min_xyz: tuple[float, float, float],
        max_xyz: tuple[float, float, float],
    ):
        """
        Define an axis-aligned bounding box in WORLD coordinates.
        Used by volumetric objects (houses, rooms, parks).
        """
        if len(min_xyz) != 3 or len(max_xyz) != 3:
            raise ValueError("Bounds must be (x, y, z) tuples")

        try:
            min_x, min_y, min_z = (float(v) for v in min_xyz)
            max_x, max_y, max_z = (float(v) for v in max_xyz)
        except Exception:
            raise ValueError("Bounds values must be numeric")

        # Normalize bounds ordering (critical safety fix)
        self.bounds = (
            (
                min(min_x, max_x),
                min(min_y, max_y),
                min(min_z, max_z),
            ),
            (
                max(min_x, max_x),
                max(min_y, max_y),
                max(min_z, max_z),
            ),
        )

    def contains_world_point(self, xyz) -> bool:
        """
        Check whether a WORLD xyz point lies inside this object's bounds.
        Returns False if bounds are undefined.
        """
        if self.bounds is None:
            return False

        try:
            x, y, z = float(xyz[0]), float(xyz[1]), float(xyz[2])
        except Exception:
            return False

        (min_x, min_y, min_z), (max_x, max_y, max_z) = self.bounds

        return (
            min_x <= x <= max_x and
            min_y <= y <= max_y and
            min_z <= z <= max_z
        )

    # -----------------------------------------
    # Observer snapshot
    # -----------------------------------------

    def snapshot(self):
        data = {
            "name": self.name,
            "position": {
                "x": self.position[0],
                "y": self.position[1],
                "z": self.position[2],
            },
        }

        if self.bounds is not None:
            data["bounds"] = {
                "min": {
                    "x": self.bounds[0][0],
                    "y": self.bounds[0][1],
                    "z": self.bounds[0][2],
                },
                "max": {
                    "x": self.bounds[1][0],
                    "y": self.bounds[1][1],
                    "z": self.bounds[1][2],
                },
            }

        return data