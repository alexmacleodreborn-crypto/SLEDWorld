# world_core/observer_bot.py

class ObserverBot:
    """
    Passive perceptual observer.

    Rules:
    - No physics
    - No interaction
    - No cognition
    - Reports only what EXISTS
    - WorldState IS the space
    """

    def __init__(self, name: str):
        self.name = name
        self.last_snapshot = {}

    # =================================================
    # PERCEPTION
    # =================================================

    def observe(self, world):
        """
        Capture a complete perceptual snapshot of the world.
        """

        self.last_snapshot = {
            "source": "observer",
            "name": self.name,
            "frame": world.frame,

            # --------------------------
            # WORLD GEOMETRY
            # --------------------------
            "places": {
                place_name: place.snapshot()
                for place_name, place in world.places.items()
            },

            # --------------------------
            # AGENTS (PHYSICAL ONLY)
            # --------------------------
            "agents": [
                agent.snapshot()
                for agent in world.agents
                if hasattr(agent, "snapshot")
            ],
        }

    # =================================================
    # SNAPSHOT ACCESS
    # =================================================

    def snapshot(self):
        """
        Return last known perceptual state.
        """
        return self.last_snapshot or {
            "source": "observer",
            "name": self.name,
            "frame": None,
        }