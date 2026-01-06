from world_core.world_object import WorldObject
from world_core.sound.sound_source import SoundSource

class TVProfile(WorldObject):
    """
    A physical television.

    - Emits sound
    - Can be controlled by a remote
    """

    def __init__(self, name, position):
        super().__init__(name=name, position=position)

        self.sound = SoundSource(
            name=f"{name}:sound",
            position=position,
            base_volume=50.0,
        )

    # ----------------------------
    # Remote controls
    # ----------------------------

    def power_on(self):
        self.sound.turn_on()

    def power_off(self):
        self.sound.turn_off()

    def volume_up(self, step=5):
        self.sound.set_volume(self.sound.base_volume + step)

    def volume_down(self, step=5):
        self.sound.set_volume(self.sound.base_volume - step)

    def snapshot(self):
        base = super().snapshot()
        base.update({
            "type": "tv",
            "sound": self.sound.snapshot(),
        })
        return base