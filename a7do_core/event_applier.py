# a7do_core/event_applier.py

def apply_event(a7do, event):
    """
    Apply a world or experience event to A7DO.
    This is the ONLY place where the external world
    is allowed to touch the internal organism.
    """

    etype = event.get("type", "experience")
    intensity = float(event.get("intensity", 0.5))
    place = event.get("place", "unknown")
    pattern = event.get("pattern", "ambient")

    # --- Update perceived world ---
    a7do.perceived.current_place = place

    # --- BODY EFFECTS (pre-cognitive) ---
    # Intensity maps into biological drives
    a7do.body.arousal = min(1.0, a7do.body.arousal + 0.3 * intensity)
    a7do.body.fatigue = min(1.0, a7do.body.fatigue + 0.2 * intensity)

    # Wetness & hunger emerge more slowly
    if etype in ("birth", "care"):
        a7do.body.wetness = min(1.0, a7do.body.wetness + 0.15 * intensity)
        a7do.body.hunger = min(1.0, a7do.body.hunger + 0.1 * intensity)

    # --- FAMILIARITY LEARNING ---
    # Familiarity is passive, not symbolic
    a7do.familiarity.observe(
        f"{place}:{pattern}",
        weight=intensity
    )

    # --- LOG (observer-visible, not internal thought) ---
    a7do.log.add(
        f"experienced pattern={pattern} place={place}"
    )