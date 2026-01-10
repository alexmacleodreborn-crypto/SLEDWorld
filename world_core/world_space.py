from dataclasses import dataclass

WEATHER_DEFAULTS = {
    "daylight": 0.6,     # 0..1
    "wind": 0.2,         # 0..1
    "rain": 0.0,         # 0..1
    "snow": 0.0,         # 0..1
    "temperature": 0.55  # normalized 0..1
}

@dataclass
class WorldSpace:
    """
    Global “sky” / weather fields.
    No agents need to understand time; it’s just a state changing with frame.
    """
    frame_counter: int = 0

    daylight: float = WEATHER_DEFAULTS["daylight"]
    wind: float = WEATHER_DEFAULTS["wind"]
    rain: float = WEATHER_DEFAULTS["rain"]
    snow: float = WEATHER_DEFAULTS["snow"]
    temperature: float = WEATHER_DEFAULTS["temperature"]

    def tick(self, frame: int):
        self.frame_counter = int(frame)
        # simple day oscillation (no “time awareness” required by agents)
        # daylight cycles very slowly with frame
        phase = (frame % 2000) / 2000.0
        self.daylight = 0.2 + 0.8 * (1.0 - abs(phase*2 - 1.0))  # triangle wave
        # keep other fields stable for now (you can expand later)

    def snapshot(self):
        return {
            "frame": self.frame_counter,
            "daylight": round(self.daylight, 3),
            "wind": round(self.wind, 3),
            "rain": round(self.rain, 3),
            "snow": round(self.snow, 3),
            "temperature": round(self.temperature, 3),
        }