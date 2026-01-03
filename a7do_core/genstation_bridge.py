"""
Gestation Bridge
----------------
Links WorldClock time to A7DO pre-birth experience and automatic birth.

World time always runs.
A7DO awareness is gated until gestation completes.
"""

from dataclasses import dataclass
from typing import Dict

# -------------------------
# Configuration constants
# -------------------------

GESTATION_DAYS = 180          # ~6 months compressed
PREBIRTH_REPLAY_INTERVAL = 6 # world-hours between consolidation cycles


@dataclass
class GestationState:
    elapsed_days: float = 0.0
    birthed: bool = False
    last_replay_hour: int = 0


class GestationBridge:
    def __init__(self, a7do, world_clock):
        self.a7do = a7do
        self.clock = world_clock
        self.state = GestationState()

    # -------------------------
    # Main update hook
    # -------------------------

    def tick(self):
        """
        Called every world tick.
        """
        if self.state.birthed:
            return

        # Advance gestation time
        self.state.elapsed_days = self.clock.days_elapsed

        # Apply pre-birth sensory exposure
        self._apply_prebirth_sensory()

        # Periodic consolidation (no wake/sleep)
        self._maybe_consolidate()

        # Automatic birth
        if self.state.elapsed_days >= GESTATION_DAYS:
            self._trigger_birth()

    # -------------------------
    # Pre-birth experience
    # -------------------------

    def _apply_prebirth_sensory(self):
        """
        Pre-symbolic exposure via mother/world.
        """
        snapshot = self.clock.snapshot()

        channels: Dict[str, float] = {
            "pressure": 0.6,
            "motion": 0.4,
            "muffled_sound": snapshot.get("ambient_noise", 0.3),
            "warmth": 0.7,
        }

        self.a7do.familiarity.observe(
            place="womb",
            channels=channels,
            intensity=0.5,
        )

        self.a7do.internal_log.append(
            "prebirth: sensory substrate active"
        )

    # -------------------------
    # Automatic consolidation
    # -------------------------

    def _maybe_consolidate(self):
        hour = int(self.clock.hours_elapsed)
        if hour - self.state.last_replay_hour >= PREBIRTH_REPLAY_INTERVAL:
            replayed = self.a7do.familiarity.replay()
            self.state.last_replay_hour = hour

            if replayed:
                self.a7do.internal_log.append(
                    f"prebirth: consolidation replay {replayed}"
                )

    # -------------------------
    # Birth transition
    # -------------------------

    def _trigger_birth(self):
        self.state.birthed = True

        # Unlock awareness
        self.a7do.mark_birthed()
        self.a7do.unlock_awareness()

        # Transition perception
        self.a7do.perceived_place = "hospital"

        self.a7do.internal_log.append(
            "birth: awareness unlocked, external world begins"
        )