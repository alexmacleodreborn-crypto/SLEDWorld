def apply_event(a7do, event):
    """
    Applies a sensory experience to A7DO.
    """

    a7do.perceived_place = event.place

    # Apply body intensity
    a7do.body.apply_intensity(event.intensity)

    # Familiarity observation
    a7do.familiarity.observe(
        place=event.place,
        channels=event.channels,
        intensity=event.intensity
    )

    a7do.log(
        f"experienced pattern place={event.place} channels={list(event.channels.keys())}"
    )