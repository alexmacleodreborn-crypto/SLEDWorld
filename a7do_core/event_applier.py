def apply_event(a7do, event: dict):
    etype = event.get("type", "experience")
    place = event.get("place", a7do.world.current_place)
    intensity = float(event.get("intensity", 0.5))
    channels = event.get("channels", {}) or {}

    # Birth transition (world event triggers internal unlock)
    if etype == "birth":
        a7do.mark_birth()

    # World perception
    a7do.world.observe(place)

    # Body modulation
    a7do.body.apply_intensity(intensity)
    a7do.body.apply_channels(channels)

    # Reflex/motor (pre-language, pre-intention)
    reflex = a7do.body.maybe_reflex()
    if reflex:
        # record as a sensory-motor experience (still pre-language)
        a7do.log.add(f"reflex: {reflex} @ {place}")

    # Familiarity imprint (gated prebirth)
    a7do.familiarity.observe(
        place=place,
        channels=channels,
        intensity=intensity
    )

    # Observer log line
    dominant = "ambient"
    if channels:
        dominant = max(channels.items(), key=lambda kv: float(kv[1]))[0]
    a7do.log.add(f"experienced pattern={dominant} place={place}")