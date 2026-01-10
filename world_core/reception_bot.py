# world_core/reception_bot.py
from typing import Dict, Any

class ReceptionBot:
    def __init__(self, name="Reception-1"):
        self.name = name
        self.registry = {"symbols":{}, "objects":{}, "places":{}, "people":{}, "animals":{}}

    def update(self, world):
        # index places and any profile-level objects
        for pname, place in world.places.items():
            self.registry["places"][pname] = {"type": getattr(place, "type", "place")}

        # index people/animals if present
        for p in getattr(world, "people", []):
            self.registry["people"][p.name] = {"age": p.age, "home": p.home_name}

        for a in getattr(world, "animals", []):
            self.registry["animals"][a.name] = {"species": a.species, "color": a.color}

    def accept_symbol(self, symbol: str):
        self.registry["symbols"][symbol] = {"status":"approved"}

    def snapshot(self) -> Dict[str, Any]:
        return {"source":"reception","name":self.name,"registry": self.registry}