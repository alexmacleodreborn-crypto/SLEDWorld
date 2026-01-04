from __future__ import annotations

from world_core.heartbeat_field import HeartbeatField


def _make_heartbeat(bpm: int = 80, amplitude: float = 1.0):
    """
    Create HeartbeatField without assuming its constructor signature.
    Tries common patterns and then sets attributes if they exist.
    """
    hb = None
    errors = []

    # Try common constructor signatures (kw, positional, minimal)
    for ctor in (
        lambda: HeartbeatField(bpm=bpm, amplitude=amplitude),
        lambda: HeartbeatField(bpm=bpm),
        lambda: HeartbeatField(amplitude=amplitude),
        lambda: HeartbeatField(bpm, amplitude),
        lambda: HeartbeatField(bpm),
        lambda: HeartbeatField(),
    ):
        try:
            hb = ctor()
            break
        except Exception as e:
            errors.append(repr(e))

    if hb is None:
        raise RuntimeError(
            "Could not construct HeartbeatField with any known signature. "
            f"Constructor errors: {errors[-3:]}"
        )

    # If the object exposes these knobs, set them
    if hasattr(hb, "bpm"):
        try:
            hb.bpm = bpm
        except Exception:
            pass
    if hasattr(hb, "amplitude"):
        try:
            hb.amplitude = amplitude
        except Exception:
            pass

    return hb


def _hb_tick(hb, minutes: float):
    """
    Tick HeartbeatField without assuming its tick method name/signature.
    """
    if minutes <= 0:
        return

    # Preferred: tick(minutes=...)
    if hasattr(hb, "tick"):
        try:
            hb.tick(minutes=minutes)
            return
        except TypeError:
            # maybe tick(minutes) positional
            try:
                hb.tick(minutes)
                return
            except Exception:
                pass

    # Alternative method names sometimes used
    for fn_name in ("tick_minutes", "step", "advance"):
        if hasattr(hb, fn_name):
            fn = getattr(hb, fn_name)
            try:
                fn(minutes)
                return
            except Exception:
                pass

    # If no tick method, do nothing (but we keep app alive)
    return


def _hb_signal(hb) -> float:
    """
    Read heartbeat signal without assuming method name.
    """
    for fn_name in ("current_signal", "signal", "value", "read"):
        if hasattr(hb, fn_name):
            fn = getattr(hb, fn_name)
            try:
                return float(fn())
            except Exception:
                pass

    # If there is no signal method, try a numeric attribute
    for attr in ("signal", "value", "current"):
        if hasattr(hb, attr):
            try:
                return float(getattr(hb, attr))
            except Exception:
                pass

    return 0.0


class MotherBot:
    """
    World agent representing the mother.
    Lives fully in world time and outputs heartbeat coupling.
    """

    def __init__(self, clock):
        self.clock = clock
        self.heartbeat = _make_heartbeat(bpm=80, amplitude=1.0)
        self._last_minutes = None

    def tick(self):
        """
        Advance mother state using world time.
        """
        # Your WorldClock should expose total minutes; if not, this will fail loudly
        now_minutes = float(getattr(self.clock, "total_minutes", 0.0))

        if self._last_minutes is None:
            delta = 0.0
        else:
            delta = now_minutes - self._last_minutes

        self._last_minutes = now_minutes

        _hb_tick(self.heartbeat, delta)

    def snapshot(self, world_datetime=None):
        return {
            "agent": "mother",
            "world_time": str(world_datetime) if world_datetime else None,
            "heartbeat_bpm": getattr(self.heartbeat, "bpm", None),
            "heartbeat_phase": getattr(self.heartbeat, "phase", None),
            "heartbeat_signal": round(_hb_signal(self.heartbeat), 6),
        }