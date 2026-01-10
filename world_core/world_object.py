class WorldObject:
    def __init__(self, name: str, position):
        self.name = name
        self.position = tuple(float(x) for x in position)
        self.bounds = None

    def set_bounds(self, min_xyz, max_xyz):
        self.bounds = (tuple(min_xyz), tuple(max_xyz))

    def contains_world_point(self, xyz):
        if self.bounds is None:
            return False
        (min_x, min_y, min_z), (max_x, max_y, max_z) = self.bounds
        x, y, z = xyz
        return (min_x <= x <= max_x) and (min_y <= y <= max_y) and (min_z <= z <= max_z)

    def snapshot(self):
        return {
            "name": self.name,
            "position": self.position,
            "bounds": self.bounds
        }