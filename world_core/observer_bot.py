# world_core/observer_bot.py

class ObserverBot:
    """
    Perceptual observer.
    Accumulates exposure only.
    """

    def __init__(self, name: str):
        self.name = name
        self.frames_observed = 0
        self.seen_places = {}
        self.heard_sounds = []

    # -------------------------------------------------
    # PERCEPTION
    # -------------------------------------------------
    def observe(self, world):
        self.frames_observed += 1

        for place in world.places.values():
            self.seen_places[place.name] = (
                self.seen_places.get(place.name, 0) + 1
            )

        for agent in world.agents:
            if hasattr(agent, "emitted_sound_level") and agent.emitted_sound_level > 0:
                self.heard_sounds.append(agent.emitted_sound_level)

    # -------------------------------------------------
    # EXPORT → INVESTIGATOR
    # -------------------------------------------------
    def export_snapshot(self):
        return {
            "observer": self.name,
            "frames": self.frames_observed,
            "seen_places": dict(self.seen_places),
            "heard_sound_events": len(self.heard_sounds),
        }

    # -------------------------------------------------
    # SNAPSHOT (UI)
    # -------------------------------------------------
    def snapshot(self):
        return {
            "agent": self.name,
            "type": "observer",
            "frames_observed": self.frames_observed,
            "seen_places": self.seen_places,
            "heard_events": len(self.heard_sounds),
        }