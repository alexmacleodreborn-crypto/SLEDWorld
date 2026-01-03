import random

class EventGenerator:
    """
    Produces low-information continuous sensory events + occasional care events.
    This does NOT 'teach'. It only emits experience candidates.
    """

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def newborn_awake_stream(self, place: str, tick_index: int, body_snapshot: dict):
        """
        Returns a list of 0..N events for this tick.
        Mostly ambient + body sensations.
        Occasionally feeding/changing/soothing prompts.
        """
        events = []

        # Ambient baseline (very low intensity, repeats a lot)
        ambient_pattern = self.rng.choice([
            "ambient-light-soft",
            "ambient-voices-muffled",
            "ambient-room-tone",
            "ambient-touch-cloth",
            "ambient-warmth",
        ])
        events.append({
            "place": place,
            "intensity": 0.6,
            "pattern": ambient_pattern
        })

        # Body sensation cues (still pre-language)
        hunger = body_snapshot["hunger"]
        wetness = body_snapshot["wetness"]
        fatigue = body_snapshot["fatigue"]

        if hunger > 0.75 and self.rng.random() < 0.7:
            events.append({
                "place": place,
                "intensity": 1.6,
                "pattern": "body-hunger-discomfort"
            })

        if wetness > 0.75 and self.rng.random() < 0.7:
            events.append({
                "place": place,
                "intensity": 1.6,
                "pattern": "body-wetness-discomfort"
            })

        if fatigue > 0.75 and self.rng.random() < 0.4:
            events.append({
                "place": place,
                "intensity": 1.2,
                "pattern": "body-heavy-eyes"
            })

        # Occasional caregiver contact as sensory (not concept)
        if self.rng.random() < 0.25:
            events.append({
                "place": place,
                "intensity": 1.1,
                "pattern": "caregiver-touch-hold"
            })

        return events