def perceived_snapshot(world, a7do):
    """
    Returns the filtered world snapshot as perceived by A7DO.
    Separates internal vs external rhythms correctly.
    """

    snapshot = {
        "place": world.current_place,
        "channels": {},
    }

    # -------------------------------------------------
    # INTERNAL – A7DO heartbeat (always present)
    # -------------------------------------------------
    snapshot["channels"]["internal_rhythm"] = 0.35

    # -------------------------------------------------
    # EXTERNAL – maternal heartbeat
    # -------------------------------------------------
    mum = world.get_bot(role="mum")

    if mum:
        distance = world.distance_between(a7do, mum)

        # Prebirth: always present
        if not a7do.birthed:
            snapshot["channels"]["maternal_rhythm"] = 0.6

        # Early postbirth: fades with distance
        elif distance < 1.5:
            snapshot["channels"]["maternal_rhythm"] = max(
                0.0, 0.5 - (distance * 0.2)
            )

    # -------------------------------------------------
    # OTHER BOTS – heartbeats (postbirth only)
    # -------------------------------------------------
    if a7do.birthed:
        for bot in world.bots:
            if bot.role in ("dad", "nurse", "doctor"):
                d = world.distance_between(a7do, bot)
                if d < 1.0:
                    snapshot["channels"]["external_rhythm"] = 0.15

    # -------------------------------------------------
    # Ambient world channels
    # -------------------------------------------------
    snapshot["channels"]["ambient"] = world.ambient_level()
    snapshot["channels"]["light"] = world.light_level()
    snapshot["channels"]["sound"] = world.sound_level()

    return snapshot