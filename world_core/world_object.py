class WorldObject:
    def __init__(self, name: str, position):
        self.name = name
        self.position = tuple(position)
        self.bounds = None

    def set_bounds(self, min_xyz, max_xyz):
        self.bounds = (tuple(min_xyz), tuple(max_xyz))

    def contains_world_point(self, xyz):
        if not self.bounds:
            return False
        (minx, miny, minz), (maxx, maxy, maxz) = self.bounds
        x, y, z = xyz
        return (minx <= x <= maxx) and (miny <= y <= maxy) and (minz <= z <= maxz)

    def snapshot(self):
        return {
            "type": "world_object",
            "name": self.name,
            "position": self.position,
            "bounds": self.bounds,
        }