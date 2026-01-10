import math


class WalkerBot:
    """
    Physical agent:
    - moves in world coordinates
    - returns to TV position every return_interval frames
    - toggles TV power (via remote press)
    """

    def __init__(self, name, start_xyz, world, speed=2.0, return_interval=15):
        self.name = name
        self.world = world
        self.xyz = tuple(start_xyz)
        self.speed = float(speed)
        self.return_interval = int(return_interval)

        self.frames = 0
        self.last = {}
        self.target = None

    @property
    def position(self):
        return self.xyz

    def _get_tv_and_remote(self):
        house = self.world.places.get("Family House")
        if not house or not hasattr(house, "rooms"):
            return None, None, None

        for room in house.rooms.values():
            if hasattr(room, "objects") and "tv" in room.objects and "remote" in room.objects:
                return room, room.objects["tv"], room.objects["remote"]

        return None, None, None

    def _move_toward(self, target_xyz):
        x, y, z = self.xyz
        tx, ty, tz = target_xyz
        dx = tx - x
        dy = ty - y
        dz = tz - z
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < 1e-6:
            return
        step = min(self.speed, dist)
        self.xyz = (x + dx/dist * step, y + dy/dist * step, z + dz/dist * step)

    def tick(self, clock):
        self.frames += 1

        room, tv, remote = self._get_tv_and_remote()
        tv_is_on = tv.is_on if tv else None

        # every return_interval frames -> go to tv and toggle
        if room and tv and remote and (self.frames % self.return_interval == 0):
            self.target = tv.position
        # if no target, wander near house
        if self.target is None:
            self.target = (self.xyz[0] + 5.0, self.xyz[1] + 2.0, self.xyz[2])

        self._move_toward(self.target)

        # if reached tv, press remote and clear target
        if tv and self.target == tv.position:
            # close enough?
            if math.dist(self.xyz, tv.position) < 1.5:
                remote.press_power()
                tv_is_on = tv.is_on
                self.target = None

        self.last = {
            "source": "walker",
            "name": self.name,
            "frame": self.world.space.frame_counter,
            "xyz": self.xyz,
            "target": self.target,
            "seen_objects": {
                "tv_is_on": tv_is_on
            }
        }

    def snapshot(self):
        return self.last or {
            "source": "walker",
            "name": self.name,
            "frame": self.frames,
            "xyz": self.xyz
        }