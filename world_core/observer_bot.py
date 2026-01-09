class ObserverBot:
    """
    Passive global observer.
    Samples physical fields.
    No cognition. No interpretation.
    """

    def __init__(self, name: str):
        self.name = name
        self.frames_observed = 0
        self.last_snapshot = {}

    # =================================================
    # PERCEPTION
    # =================================================

    def observe(self, world):
        """
        Sample global physical state.
        """
        self.frames_observed += 1

        rooms_report = []

        for place in world.places.values():
            if not hasattr(place, "rooms"):
                continue

            for room in place.rooms.values():
                rooms_report.append({
                    "room": room.name,
                    "sound_level": room.get_sound_level(),
                    "light_level": room.get_light_level(),
                })

        self.last_snapshot = {
            "source": "observer",
            "frames_observed": self.frames_observed,
            "rooms": rooms_report,
        }

    # =================================================
    # SNAPSHOT (FOR INVESTIGATOR)
    # =================================================

    def snapshot(self):
        return self.last_snapshot