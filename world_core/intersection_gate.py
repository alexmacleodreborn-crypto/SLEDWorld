# world_core/intersection_gate.py

def perceived_snapshot(world, a7do):
    """
    Intersection gate between objective world state and A7DO perception.

    Rules:
    - World always exists fully.
    - A7DO only receives a reduced, gated snapshot.
    - Pre-birth: heavily muted, no discrete objects.
    - Post-birth: gradual unlocking.
    """

    # Base environmental signals from world
    env = world.environment_snapshot()

    # Gating factor
    if not a7do.birthed:
        gate = 0.3
    else:
        gate = 1.0

    snapshot = {
        "place": env.get("place", "unknown"),
        "light": env.get("light", 0.0) * gate,
        "sound": env.get("sound", 0.0) * gate,
        "motion": env.get("motion", 0.0) * gate,
        "touch": env.get("touch", 0.0) * gate,
        "temperature": env.get("temperature", 0.0) * gate,
        "smell": env.get("smell", 0.0) * gate,
    }

    # No objects, no language, no symbols here
    # Those come later via familiarity + consolidation

    return snapshot