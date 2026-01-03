# a7do_core/event_applier.py

def apply_event(a7do, event: dict):
    """
    Applies a sensory event to A7DO.
    World meaning is NOT interpreted here.
    """

    place = event.get("place", "—")
    channels = event.get("channels", {})
    intensity = float(event.get("intensity", 0.0))

    # Body reacts first
    a7do.body.apply_intensity(intensity)

    # Familiarity observes pattern (pre-symbolic)
    a7do.familiarity.observe(
        place=place,
        channels=channels,
        intensity=intensity
    )

    a7do.internal_log.append(
        f"experienced pattern place={place} channels={list(channels.keys())}"
    )