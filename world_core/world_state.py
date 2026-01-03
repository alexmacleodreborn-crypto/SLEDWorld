class WorldState:
    """
    Objective world state.
    Exists independently of A7DO awareness.
    """

    def __init__(self):
        self.initialised = False
        self.time_minutes = 0.0

        # Global environment (objective)
        self.environment = {
            "light": 0.5,     # 0–1 ambient brightness
            "sound": 0.4,     # ambient noise
            "motion": 0.3,    # movement in environment
            "temperature": 0.5,
        }

        # Places exist before A7DO perceives them
        self.places = {
            "hospital": {"active": True},
            "home": {"active": False},
            "park": {"active": False},
            "street": {"active": False},
        }

        # Living entities in the world
        self.bots = {}

    def initialise(self):
        """
        Bootstraps the world before A7DO awareness.
        """
        self.initialised = True

    def tick(self, minutes: float):
        """
        Advances world time and environment.
        """
        self.time_minutes += minutes

        # Simple diurnal-like cycle without naming it
        phase = (self.time_minutes % 1440) / 1440.0

        self.environment["light"] = 0.3 + 0.7 * abs(0.5 - phase) * 2
        self.environment["sound"] = 0.3 + 0.2 * (phase > 0.4 and phase < 0.6)
        self.environment["motion"] = 0.2 + 0.3 * (phase > 0.3 and phase < 0.7)

    def snapshot(self):
        """
        Observer-visible world snapshot.
        """
        return {
            "time_minutes": round(self.time_minutes, 2),
            "environment": {k: round(v, 3) for k, v in self.environment.items()},
            "active_places": [
                p for p, v in self.places.items() if v.get("active")
            ],
            "bots": list(self.bots.keys()),
        }