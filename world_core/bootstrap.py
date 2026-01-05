from world_core.world_state import WorldState
from world_core.profiles.park_profile import ParkProfile


def build_world():
    world = WorldState(acceleration=60)

    # Create a park
    park = ParkProfile(
        name="central_park",
        position=(500, 500, 0),
    )

    world.places["park"] = park

    return world