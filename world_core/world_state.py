class WorldState:
    """
    Canonical world container.

    - Holds all places
    - Holds all static world objects
    - No agents
    - No perception
    - No cognition
    """

    def __init__(self):
        # Places indexed by name
        self.places: dict[str, object] = {}

    # -------------------------
    # Place management
    # -------------------------

    def add_place(self, place):
        """
        Register a place in the world.
        """
        if place.name in self.places:
            raise ValueError(f"Place already exists: {place.name}")

        self.places[place.name] = place

    # -------------------------
    # Observer snapshot
    # -------------------------

    def snapshot(self):
        """
        Full world snapshot (observer only).
        """
        return {
            "places": {
                name: place.snapshot()
                for name, place in self.places.items()
            }
        }