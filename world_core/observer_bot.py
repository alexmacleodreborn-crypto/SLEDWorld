class ObserverBot:
    """
    Passive perception layer.
    """
    def __init__(self, name="Observer"):
        self.name = name
        self.last = {}

    def observe(self, world):
        # Observe world space + a small summary of emitters (no heavy payloads)
        self.last = {
            "source": "observer",
            "name": self.name,
            "frame": world.frame,
            "world_space": world.space.snapshot() if hasattr(world, "space") else {},
            "places_seen": list(world.places.keys())[:10],
        }

    def snapshot(self):
        return self.last or {"source": "observer", "name": self.name}