class RemoteProfile:
    def __init__(self, name, position, tv):
        self.name = name
        self.position = tuple(position)
        self.tv = tv

    def power_toggle(self):
        return self.tv.power_toggle()

    def snapshot(self):
        return {
            "type": "remote",
            "name": self.name,
            "position": self.position,
            "bound_to": getattr(self.tv, "name", "tv"),
        }