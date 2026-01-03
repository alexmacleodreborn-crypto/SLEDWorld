from typing import Dict, Any


def perceived_snapshot(world, a7do) -> Dict[str, Any]:
    """
    The ONLY place external world becomes perceivable.
    Produces a minimal perceived snapshot for A7DO:
      {
        "place": str,
        "channels": { name: float }
      }
    """

    place = getattr(world, "current_place", "—")

    channels: Dict[str, float] = {}

    # -------------------------
    # INTERNAL (A7DO): always present
    # -------------------------
    channels["internal_rhythm"] = 0.35

    # -------------------------
    # Ambient world channels
    # -------------------------
    channels["ambient"] = float(world.ambient_level())
    channels["light"] = float(world.light_level())
    channels["sound"] = float(world.sound_level())

    # -------------------------
    # Maternal rhythm rules
    # -------------------------
    mum = world.get_bot("mum")
    if mum is not None:
        d = world.distance_between_a7do_and(mum)

        # Prebirth: mum is always the external anchor
        if not a7do.birthed:
            channels["maternal_rhythm"] = 0.60

        # Postbirth: fades with distance (close holding matters)
        else:
            if d < 1.5:
                channels["maternal_rhythm"] = max(0.0, 0.50 - 0.20 * d)

    # -------------------------
    # Other human rhythms (postbirth only, low salience)
    # -------------------------
    if a7do.birthed:
        for role in ("dad", "nurse", "doctor"):
            b = world.get_bot(role)
            if b is None:
                continue
            d = world.distance_between_a7do_and(b)
            if d < 1.0:
                # kept weak: usually masked by ambient sound
                channels["external_rhythm"] = max(float(channels.get("external_rhythm", 0.0)), 0.12)

    return {"place": place, "channels": channels}