from .world_state import WorldState, Place
from .bot import Bot

def bootstrap_world() -> WorldState:
    world = WorldState()

    world.places["hospital"] = Place(
        name="Hospital",
        kind="hospital",
        ambient_noise="machines voices",
        smells=["clean", "antiseptic"],
        light_level=0.9,
    )

    world.places["home"] = Place(
        name="Home",
        kind="home",
        ambient_noise="quiet",
        smells=["fabric", "food"],
        light_level=0.6,
    )

    world.bots["Mum"] = Bot("Mum", "mum", "hospital")
    world.bots["Dad"] = Bot("Dad", "dad", "hospital")

    return world