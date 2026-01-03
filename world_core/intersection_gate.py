import random
import math

# Independent phase for maternal heartbeat
_maternal_phase = random.uniform(0, 2 * math.pi)
_maternal_rate = random.uniform(1.0, 1.4)  # adult resting bpm range


def sample_world(world, focus_place: str):
    global _maternal_phase

    place = world.places[focus_place]

    # External heartbeat (mother)
    _maternal_phase += _maternal_rate * 0.08
    maternal_pulse = abs(math.sin(_maternal_phase)) * 0.2

    return {
        "place": place.name,
        "channels": {
            "ambient": 0.3,
            "light": place.light_level * 0.5,
            "maternal_heartbeat": maternal_pulse,
        },
    }