class WorldGrid:
    """
    Minimal registry. You can extend to spatial indexing later.
    """
    def __init__(self):
        self.objects = []

    def register(self, obj):
        self.objects.append(obj)