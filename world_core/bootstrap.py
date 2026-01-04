from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot

def build_world():
    clock = WorldClock(acceleration=60)

    places = {
        "hospital": {
            "type": "indoor",
            "noise": 0.6,
            "light": 0.8,
        },
        "home": {
            "type": "indoor",
            "noise": 0.3,
            "light": 0.5,
        },
        "park": {
            "type": "outdoor",
            "noise": 0.7,
            "light": 1.0,
        },
    }

    agents = {
        "mother": MotherBot(clock),
    }

    return {
        "clock": clock,
        "agents": agents,
        "places": places,   # ✅ THIS IS THE MISSING PIECE
    }