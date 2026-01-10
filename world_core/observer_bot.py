class ObserverBot:
    """
    Passive cognitive sensor:
    - sees objects and their light signatures
    - hears sound in rooms
    """
    def __init__(self, name="Observer"):
        self.name = name
        self.frames = 0
        self.last = {}

    def observe(self, world):
        self.frames += 1

        # Find "Family House" and its living room
        house = world.places.get("Family House")
        seen = {"places": list(world.places.keys())}
        heard = {"sound_level": 0.0}
        light = {"light_level": 0.0}

        tv_is_on = None
        tv_light_color = None

        if house and hasattr(house, "rooms"):
            for room in house.rooms.values():
                # collect room signatures
                if hasattr(room, "get_sound_level"):
                    heard["sound_level"] = max(heard["sound_level"], room.get_sound_level())
                if hasattr(room, "get_light_level"):
                    light["light_level"] = max(light["light_level"], room.get_light_level())

                # TV state
                tv = room.objects.get("tv") if hasattr(room, "objects") else None
                if tv:
                    tv_is_on = tv.is_on
                    tv_light_color = tv.light.color

        self.last = {
            "source": "observer",
            "name": self.name,
            "frame": world.space.frame_counter,
            "world_space": world.space.snapshot(),
            "seen": light,
            "heard": heard,
            "seen_objects": {
                "tv_is_on": tv_is_on,
                "tv_light_color": tv_light_color,
            },
        }

    def snapshot(self):
        return self.last or {
            "source": "observer",
            "name": self.name,
            "frame": self.frames
        }