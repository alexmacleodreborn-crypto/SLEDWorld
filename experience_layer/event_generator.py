from .experience_event import ExperienceEvent
from world_core.intersection_gate import sample_world

def generate_event(world, focus_place):
    snapshot = sample_world(world, focus_place)

    return ExperienceEvent(
        source="world",
        payload=snapshot,
        intensity=1.0,
    )