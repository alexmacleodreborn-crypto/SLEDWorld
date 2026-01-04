from world_core.world_clock import WorldClock
from world_core.world_state import WorldState
from world_core.place import Place
from world_core.agent_base import Agent

def build_world():
    clock = WorldClock(acceleration=120)

    world = WorldState(clock)

    # Places
    home = Place("Home")
    park = Place("Park")
    shop = Place("Shop")

    for p in (home, park, shop):
        world.add_place(p)

    # Agents
    mum = Agent("Mum", "adult")
    dad = Agent("Dad", "adult")
    dog = Agent("Dog", "animal")

    world.add_agent(mum, "Home")
    world.add_agent(dad, "Home")
    world.add_agent(dog, "Home")

    return world