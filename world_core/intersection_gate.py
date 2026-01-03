def sample_world(world, focus_place: str):
    place = world.places[focus_place]

    return {
        "place": place.name,
        "noise": place.ambient_noise,
        "smells": place.smells,
        "light": place.light_level,
        "time": world.time_of_day,
    }