import math


class ScoutBot:
    """
    Local square-grid scout:
    - samples occupancy (shape), sound grid, light grid in a square around center_xyz
    - outputs grids into snapshot for Streamlit rendering
    """

    def __init__(self, name, center_xyz, extent_m=18.0, resolution_m=2.0, max_frames=200):
        self.name = name
        self.center_xyz = tuple(center_xyz)
        self.extent_m = float(extent_m)
        self.resolution_m = float(resolution_m)
        self.max_frames = int(max_frames)

        self.frames = 0
        self.active = True
        self.last = {}

    def _sample_room_signatures(self, world, x, y, z):
        """
        Return (occupancy, sound, light) sampled at this point.
        """
        occ = 0.0
        sound = 0.0
        light = 0.0

        for place in world.places.values():
            # occupancy if inside any place bounds
            if hasattr(place, "contains_world_point") and place.contains_world_point((x, y, z)):
                occ = 1.0

            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point((x, y, z)):
                        occ = 1.0
                        sound = max(sound, getattr(room, "get_sound_level", lambda: 0.0)())
                        light = max(light, getattr(room, "get_light_level", lambda: 0.0)())

                        # enrich by TV local field: if close to TV, raise the grid
                        tv = room.objects.get("tv") if hasattr(room, "objects") else None
                        if tv:
                            d = math.dist((x, y, z), tv.position)
                            if d < 12:
                                sound = max(sound, tv.sound.level() * (1.0 - d / 12.0))
                                light = max(light, tv.light.level() * (1.0 - d / 12.0))

        return occ, round(sound, 3), round(light, 3)

    def observe(self, world):
        if not self.active:
            return
        self.frames += 1
        if self.frames > self.max_frames:
            self.active = False
            return

        cx, cy, cz = self.center_xyz
        r = self.extent_m
        step = self.resolution_m

        n = int((2 * r) / step)
        if n <= 0:
            n = 1

        occupancy = [[0.0 for _ in range(n)] for __ in range(n)]
        sound_grid = [[0.0 for _ in range(n)] for __ in range(n)]
        light_grid = [[0.0 for _ in range(n)] for __ in range(n)]

        for iy in range(n):
            y = cy - r + iy * step
            for ix in range(n):
                x = cx - r + ix * step
                occ, snd, lgt = self._sample_room_signatures(world, x, y, cz)
                occupancy[iy][ix] = occ
                sound_grid[iy][ix] = snd
                light_grid[iy][ix] = lgt

        self.last = {
            "source": "scout",
            "name": self.name,
            "frame": world.space.frame_counter,
            "active": self.active,
            "grid_size": n,
            "resolution": step,
            "occupancy": occupancy,
            "sound_grid": sound_grid,
            "light_grid": light_grid,
        }

    def snapshot(self):
        return self.last or {
            "source": "scout",
            "name": self.name,
            "frame": self.frames,
            "active": self.active,
        }