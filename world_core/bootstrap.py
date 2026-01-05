from world_core.world_state import WorldState
from world_core.profiles import (
    ParkProfile,
    HouseProfile,
    RoadProfile,
    ShopProfile,
    HospitalProfile,
)


def build_world() -> WorldState:
    world = WorldState()

    # Core places
    world.add_place(ParkProfile(
        name="central_park",
        position=(500, 500, 0),
    ))

    world.add_place(HospitalProfile(
        name="city_hospital",
        position=(200, 800, 0),
    ))

    # Residential
    for i in range(10):
        world.add_place(HouseProfile(
            name=f"house_{i}",
            position=(100 + i * 60, 100, 0),
        ))

    # Roads
    world.add_place(RoadProfile(
        name="main_road",
        position=(300, 300, 0),
    ))

    # Shops
    world.add_place(ShopProfile(
        name="grocery_store",
        position=(450, 320, 0),
    ))

    return world