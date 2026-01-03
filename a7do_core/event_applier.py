def apply_event(a7do, event: dict):
    """
    Apply a single event to A7DO.
    Heartbeat is treated as a continuous background signal.
    """

    # -------------------------
    # Extract event fields
    # -------------------------

    event_type = event.get("type", "unknown")
    place = event.get("place", "—")
    intensity = float(event.get("intensity", 0.0))
    channels = dict(event.get("channels", {}))

    # -------------------------
    # Inject internal heartbeat (always present)
    # -------------------------

    # Internal body rhythm – never gated off
    channels.setdefault("internal_rhythm", 0.35)

    # -------------------------
    # Inject maternal heartbeat (prebirth / early)
    # -------------------------

    if getattr(a7do, "prebirth", False) or not a7do.birthed:
        channels.setdefault("maternal_rhythm", 0.55)

    # -------------------------
    # Body-level processing
    # -------------------------

    if hasattr(a7do, "body"):
        a7do.body.apply_intensity(intensity)

    # -------------------------
    # Familiarity imprinting
    # -------------------------

    if hasattr(a7do, "familiarity"):
        a7do.familiarity.observe(
            place=place,
            channels=channels,
            intensity=intensity,
        )

    # -------------------------
    # Internal observer log
    # -------------------------

    dominant = "ambient"
    if channels:
        dominant = max(channels.items(), key=lambda kv: kv[1])[0]

    a7do.internal_log.append(
        f"experienced pattern={dominant} place={place}"
    )

    # -------------------------
    # Special hooks
    # -------------------------

    if event_type == "birth":
        a7do.internal_log.append("high-intensity sensory onset")