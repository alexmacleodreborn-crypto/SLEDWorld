def sleep_consolidate(a7do):
    """
    Sleep replay (still pre-language):
    - reinforce familiar patterns
    - lightly dampen arousal
    """
    a7do.log.add("sleep: replay and consolidation")

    # reinforce top familiar patterns slightly (stability)
    top = a7do.familiarity.top(5)
    for pattern, score in top:
        # small replay reinforcement
        a7do.familiarity.reinforce(pattern, amount=0.2)
        a7do.log.add(f"sleep-replay: {pattern}")

    # body sleep ticks simulate settling
    for _ in range(6):
        a7do.body.sleep_tick(dt=1.0)