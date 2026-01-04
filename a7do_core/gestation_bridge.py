# sledworld/a7do_core/gestation_bridge.py

class GestationBridge:
    """
    Couples *world* mother signals into *A7DO* prebirth sensory inputs.

    Design rules:
    - Safe to import (NO heavy imports, NO dataclass defaults).
    - A7DO has no world-time awareness.
    - We only feed pre-symbolic sensory patterns.
    """

    def __init__(self, a7do, mother, clock, gestation_days: int = 280):
        self.a7do = a7do
        self.mother = mother
        self.clock = clock

        self.gestation_days = int(gestation_days)

        self.completed = False
        self.elapsed_days = 0.0
        self.phase = "prebirth"  # prebirth -> birth_ready -> completed

        # internal guard so we only unlock once
        self._birth_unlocked = False

    def _compute_elapsed_days(self) -> float:
        """
        Derive elapsed days from the world clock without requiring any specific clock API.
        Supports:
        - clock.total_minutes
        - clock.minutes_elapsed
        - clock.snapshot()["total_minutes"]
        - fallback: 0.0
        """
        # direct attributes first
        for attr in ("total_minutes", "minutes_elapsed"):
            if hasattr(self.clock, attr):
                mins = float(getattr(self.clock, attr))
                return mins / 1440.0

        # snapshot fallback
        if hasattr(self.clock, "snapshot"):
            snap = self.clock.snapshot()
            if isinstance(snap, dict):
                if "total_minutes" in snap:
                    return float(snap["total_minutes"]) / 1440.0
                if "minutes_elapsed" in snap:
                    return float(snap["minutes_elapsed"]) / 1440.0

        return 0.0

    def tick(self):
        """
        Called each UI tick.
        - updates elapsed days
        - feeds A7DO prebirth sensory drip
        - advances body micro-motion
        - triggers birth unlock when ready
        """
        if self.completed:
            return

        # 1) update elapsed days from world time
        self.elapsed_days = self._compute_elapsed_days()

        # 2) Mother signal -> prebirth sensory channels
        # mother must provide a dict via sensory_snapshot(); if not, fallback safe.
        if hasattr(self.mother, "sensory_snapshot"):
            mother_signal = self.mother.sensory_snapshot()
        else:
            mother_signal = {"heartbeat": 0.0, "motion": 0.0, "sound": 0.0}

        # Build channels for familiarity (pre-symbolic)
        channels = {
            "heartbeat": float(mother_signal.get("heartbeat", 0.0)),
            "motion": float(mother_signal.get("motion", 0.0)),
            "sound": float(mother_signal.get("sound", 0.0)),
        }

        # intensity is coarse energy proxy (kept small prebirth)
        intensity = min(1.0, 0.2 + 0.3 * channels["heartbeat"] + 0.2 * channels["motion"] + 0.2 * channels["sound"])

        # 3) Apply into A7DO substrate (NO language)
        # Familiarity class can be Familiarity or FamiliarityTracker; use observe() if present.
        if hasattr(self.a7do, "familiarity") and hasattr(self.a7do.familiarity, "observe"):
            self.a7do.familiarity.observe(
                place="womb",
                channels=channels,
                intensity=float(intensity),
            )

        # 4) Body tick always runs (prebirth motion/contact patterns)
        if hasattr(self.a7do, "body") and hasattr(self.a7do.body, "tick"):
            self.a7do.body.tick()

        # 5) Gate: when gestation threshold reached -> birth unlock
        if self.elapsed_days >= self.gestation_days:
            self.phase = "birth_ready"
            if (not self._birth_unlocked) and hasattr(self.a7do, "unlock_awareness"):
                self.a7do.unlock_awareness()
                self._birth_unlocked = True
                if hasattr(self.a7do, "internal_log"):
                    self.a7do.internal_log.append("gestation: threshold reached -> birth gate opened")

            self.completed = True
            self.phase = "completed"