# world_core/world_object.py

class WorldObject:
    """
    Pure physical object.
    """

    def __init__(self, obj_id, obj_type, position, size, material):
        self.id = obj_id
        self.type = obj_type
        self.position = position  # (x, y, z)
        self.size = size          # (dx, dy, dz)
        self.material = material

    def bounds(self):
        x, y, z = self.position
        dx, dy, dz = self.size
        return (x, x+dx, y, y+dy, z, z+dz)

    def snapshot(self):
        return {
            "id": self.id,
            "type": self.type,
            "position": self.position,
            "size": self.size,
            "material": self.material.name,
        }