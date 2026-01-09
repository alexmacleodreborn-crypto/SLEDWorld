class ObserverBot:
    """
    Passive observer.
    Does not move.
    Does not act.
    Does not depend on clock.
    Only records what persists in the world.
    """

    def __init__(self, name="observer"):
        self.name = name
        self.seen_places = {}
        self.frames_observed = 0

    def observe(self, world):
        """
        Observe the world without changing it.
        """
        self.frames_observed += 1

        for place_name in world.places.keys():
            self.seen_places.setdefault(place_name, 0)
            self.seen_places[place_name] += 1

    def snapshot(self):
        """
        Return observer memory.
        """
        return {
            "name": self.name,
            "frames_observed": self.frames_observed,
            "seen_places": dict(self.seen_places),
        }