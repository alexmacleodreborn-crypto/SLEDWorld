# world_core/world_space.py

from dataclasses import dataclass

@dataclass
class WorldWeather:
    # simple toggles; no “time”, only state + frame
    sun_level: float = 0.6      # 0..1
    rain: bool = False
    snow: bool = False
    wind: float = 0.2           # 0..1
    cloud: float = 0.2          # 0..1

class WorldSpace:
    """
    Global environment. Frame-based. No cognitive meaning.
    """
    def __init__(self):
        self.frame_counter = 0
        self.weather = WorldWeather()

    def tick(self, frame: int):
        self.frame_counter = int(frame)

        # simple cyclic-ish variation without time meaning
        # (just a deterministic state evolution)
        f = self.frame_counter
        self.weather.sun_level = 0.3 + 0.3 * ((f % 100) / 100.0)  # 0.3..0.6
        self.weather.cloud = 0.1 + 0.5 * (((f * 7) % 100) / 100.0)
        self.weather.wind = 0.1 + 0.6 * (((f * 13) % 100) / 100.0)

        # occasional toggles (rare)
        self.weather.rain = ((f % 240) > 200)
        self.weather.snow = ((f % 500) > 470)

    def snapshot(self):
        return {
            "frame_counter": self.frame_counter,
            "weather": {
                "sun_level": round(self.weather.sun_level, 3),
                "cloud": round(self.weather.cloud, 3),
                "wind": round(self.weather.wind, 3),
                "rain": self.weather.rain,
                "snow": self.weather.snow,
            }
        }