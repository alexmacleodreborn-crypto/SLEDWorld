def apply_event(a7do, event):
    """
    Applies a single experience event to A7DO.
    Order is critical:
      1. Body
      2. Familiarity
      3. Observer trace
    """

    # 1. Somatic impact (reflexive, local)
    a7do.body.apply_intensity(event.intensity)

    # 2. Pre-symbolic familiarity imprint
    a7do.familiarity.observe(
        place=event.payload.get("place", "—"),
        channels=event.payload.get("channels", {}),
        intensity=event.intensity,
    )

    # 3. Observer-visible phenomenology
    a7do.log(
        f"experienced pattern={a7do.familiarity.last_pattern}"
    )