class ReceptionBot:
    """
    Indexes world entities into a registry (names are not “understood”, just stored).
    """
    def __init__(self):
        self.registry = {"places": {}, "rooms": {}, "objects": {}}
        self.accepted_symbols = []

    def accept_symbol(self, sym):
        self.accepted_symbols.append(sym)

    def update(self, world):
        # places
        for name, place in world.places.items():
            self.registry["places"][name] = getattr(place, "snapshot", lambda: {"name": name})()

            # rooms/objects if present
            if hasattr(place, "rooms"):
                for rname, room in place.rooms.items():
                    self.registry["rooms"][rname] = room.snapshot()
                    if hasattr(room, "objects"):
                        for oname, obj in room.objects.items():
                            # may not have snapshot
                            if hasattr(obj, "snapshot"):
                                self.registry["objects"][f"{rname}:{oname}"] = obj.snapshot()
                            else:
                                self.registry["objects"][f"{rname}:{oname}"] = {"name": str(obj)}

    def snapshot(self):
        return {
            "source": "reception",
            "counts": {
                "places": len(self.registry["places"]),
                "rooms": len(self.registry["rooms"]),
                "objects": len(self.registry["objects"]),
            }
        }