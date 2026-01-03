from .experience_event import ExperienceEvent
from world_core.intersection_gate import sample_world


def sensory_drip(world, focus_place: str):
    """
    Low-intensity continuous sensory exposure.
    This is NOT an 'event' like birth or travel.
    It is background existence.
    """
    snapshot = sample_world(world, focus_place)

    return ExperienceEvent(
        source="world:drip",
        payload={
            "place": snapshot["place"],
            "channels": {
                "noise": 0.3,
                "light": snapshot["light"] * 0.5,
            },
        },
        intensity=0.25,
    )