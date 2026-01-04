def basic_adult_schedule(agent, clock):
    hour = clock.world_datetime.hour

    if 7 <= hour < 9:
        return "commute"
    if 9 <= hour < 17:
        return "work"
    if 17 <= hour < 22:
        return "home"
    return "sleep"