def sensory_drip(snapshot, *, base_intensity=0.15):
    """
    Continuous low-level sensory input.
    Used for prebirth, sleep, and passive awareness.
    """

    channels = snapshot.get("channels", {})

    # Safe extraction
    ambient = float(channels.get("ambient", 0.2))
    light = float(channels.get("light", 0.0))
    maternal_hb = float(channels.get("maternal_heartbeat", 0.0))

    return {
        "place": snapshot.get("place", "—"),
        "channels": {
            "ambient": ambient * 0.6,
            "light": light * 0.5,
            "maternal_heartbeat": maternal_hb,
        },
        "intensity": base_intensity,
    }