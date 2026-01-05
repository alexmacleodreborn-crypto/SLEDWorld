# world_core/bootstrap.py

from world_core.world_space import WorldSpace
from world_core.place import Place
from world_core.profiles.park_profile import ParkProfile

def build_world():
    world = WorldSpace()

    park = Place(
        name="Central Park",
        origin=(1000, 1000, 0),
        size=(200, 200, 0),
        profile=ParkProfile(tree_count=20),
    )

    park.populate()

    for obj in park.objects:
        world.add_object(obj)

    return world