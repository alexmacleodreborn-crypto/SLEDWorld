import random
from typing import Dict, Any, List


class ExperienceGenerator:
    """
    Generates continuous micro-experiences (events) while A7DO is awake,
    and also generates muted pre-birth experience (fetal substrate).

    IMPORTANT:
    - Does not decide meaning.
    - Does not invent world facts.
    - Only converts perceived snapshots into event dicts.
    """

    def __init__(self, seed: int = 7):
        self.rng = random.Random(seed)
        self.last_events: List[Dict[str, Any]] = []

    def _jitter(self, x: float, amt: float = 0.05) -> float:
        return max(0.0, min(1.0, x + self.rng.uniform(-amt, amt)))

    def step(self, *, a7do, perceived: Dict[str, Any], dt: float = 0.25) -> Dict[str, Any]:
        """
        Produce a single micro-event (or none) based on:
        - A7DO lifecycle stage (prebirth/birthed)
        - awake/asleep
        - perceived snapshot from intersection gate

        Returns:
          event dict OR None
        """
        place = perceived.get("place", "—")
        channels = dict(perceived.get("channels", {}))

        # Prebirth: always-on muted substrate (even when "asleep")
        if not a7do.birthed:
            base_intensity = 0.25
            # keep it muffled, gentle drift
            channels = {k: self._jitter(float(v), 0.03) for k, v in channels.items()}
            intensity = self._jitter(base_intensity, 0.03)

            return {
                "type": "prebirth_drift",
                "place": place,
                "intensity": intensity,
                "channels": channels,
            }

        # Postbirth: only generate experiences while awake
        if not a7do.is_awake:
            return None

        # Awake micro-events: small fluctuations, occasional spikes
        ambient = float(channels.get("ambient", 0.2))
        light = float(channels.get("light", 0.2))
        sound = float(channels.get("sound", 0.2))

        # Add subtle continuous variation (life is never static)
        channels["ambient"] = self._jitter(ambient, 0.05)
        channels["light"] = self._jitter(light, 0.07)
        channels["sound"] = self._jitter(sound, 0.07)

        # Occasionally introduce a mild novelty bump
        if self.rng.random() < 0.12:
            bump_channel = self.rng.choice(list(channels.keys())) if channels else "ambient"
            channels[bump_channel] = max(channels.get(bump_channel, 0.2), 0.65)

        # Intensity is a gentle function of perceived stimulation
        intensity = 0.15 + 0.35 * max(channels.values()) if channels else 0.2
        intensity = self._jitter(float(intensity), 0.05)

        return {
            "type": "micro_experience",
            "place": place,
            "intensity": intensity,
            "channels": channels,
        }

    def run_block(self, *, a7do, perceived_provider, steps: int = 10, dt: float = 0.25) -> List[Dict[str, Any]]:
        """
        Run multiple micro-steps and return generated events.
        perceived_provider() must return a perceived snapshot dict each step.
        """
        out: List[Dict[str, Any]] = []
        self.last_events = []

        for _ in range(int(steps)):
            perceived = perceived_provider()
            ev = self.step(a7do=a7do, perceived=perceived, dt=dt)
            if ev is not None:
                out.append(ev)

        self.last_events = out[-25:]
        return out