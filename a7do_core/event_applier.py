def apply_event(a7do, event: dict):
    """
    Apply a perceived event to A7DO.

    This function assumes:
    - The event has already passed through the world → perception gate
    - All channels represent *what A7DO can perceive*, not objective reality
    - No signal is invented here (especially heartbeats)

    Event format (dict):
    {
        "type": str,
        "place": str,
        "intensity": float,
        "channels": dict[str, float]
    }
    """

    # -------------------------
    # Extract event fields safely
    # -------------------------

    event_type = event.get("type", "unknown")
    place = event.get("place", "—")
    intensity = float(event.get("intensity", 0.0))
    channels = dict(event.get("channels", {}))

    # -------------------------
    # Body-level processing
    # -------------------------

    if hasattr(a7do, "body"):
        a7do.body.apply_intensity(intensity)

    # -------------------------
    # Pre-symbolic familiarity imprint
    # -------------------------

    if hasattr(a7do, "familiarity"):
        a7do.familiarity.observe(
            place=place,
            channels=channels,
            intensity=intensity,
        )

    # -------------------------
    # Observer-visible internal log
    # -------------------------

    dominant = "ambient"
    if channels:
        dominant = max(channels.items(), key=lambda kv: kv[1])[0]

    a7do.internal_log.append(
        f"experienced pattern={dominant} place={place}"
    )

    # -------------------------
    # Special event annotations
    # -------------------------

    if event_type == "birth":
        a7do.internal_log.append("high-intensity sensory onset")