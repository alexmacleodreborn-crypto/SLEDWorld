# world_core/region.py

class Region:
    """
    Sparse spatial container.
    """

    def __init__(self, key):
        self.key = key
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def snapshot(self):
        return {
            "region": self.key,
            "object_count": len(self.objects),
        }