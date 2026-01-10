import random


class WorldSpace:
    """
    Global environment: weather-like fields.
    No agent knows 'time' – only coordinates and current state.
    """

    def __init__(self):
        self.frame_counter = 0

        # simple toggles (can later be made cyclic)
        self.sunlight = 1.0   # 0..1
        self.wind = 0.2       # 0..1
        self.rain = False
        self.snow = False
        self.temperature_c = 12.0

    def tick(self):
        self.frame_counter += 1

        # mild drift
        self.wind = max(0.0, min(1.0, self.wind + random.uniform(-0.02, 0.02)))
        self.temperature_c += random.uniform(-0.05, 0.05)

        # occasional weather flips
        if self.frame_counter % 120 == 0:
            self.rain = random.random() < 0.25
            self.snow = (not self.rain) and (random.random() < 0.08)

        # sunlight depends on rain/snow
        base = 1.0
        if self.rain:
            base *= 0.6
        if self.snow:
            base *= 0.75
        self.sunlight = base

    def snapshot(self):
        return {
            "frame": self.frame_counter,
            "sunlight": round(self.sunlight, 3),
            "wind": round(self.wind, 3),
            "rain": bool(self.rain),
            "snow": bool(self.snow),
            "temperature_c": round(self.temperature_c, 2),
        }