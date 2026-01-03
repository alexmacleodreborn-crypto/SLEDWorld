def apply_event(a7do, event):
    """
    Applies a single experience event to A7DO.
    Heartbeats run regardless of sleep.
    """

    # 🫀 Internal heartbeat always runs
    internal_pulse = a7do.body.internal_heartbeat()

    # Somatic intensity from event
    a7do.body.apply_intensity(event.intensity)

    # Reflexive movement only if awake
    if a7do.is_awake and event.intensity > 0.1:
        region, _ = a7do.body.reflex_move()
        a7do.log(f"reflex movement: {region}")

    # Familiarity (external world)
    a7do.familiarity.observe(
        place=event.payload.get("place", "—"),
        channels=event.payload.get("channels", {}),
        intensity=event.intensity,
    )

    # Observer-visible phenomenology
    a7do.log(
        f"experienced pattern={a7do.familiarity.last_pattern}"
    )