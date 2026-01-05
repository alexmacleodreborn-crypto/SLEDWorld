# world_core/place.py

class Place:
    """
    A real-world location (park, house, road).
    """

    def __init__(self, name, origin, size, profile):
        self.name = name
        self.origin = origin
        self.size = size
        self.profile = profile
        self.objects = []

    def populate(self):
        self.objects = self.profile.generate(self.origin, self.size)

    def snapshot(self):
        return {
            "place": self.name,
            "object_count": len(self.objects),
            "profile": self.profile.name,
        }