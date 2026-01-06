import math

class SoundField:
    """
    Computes sound intensity at a point in space.
    """

    @staticmethod
    def intensity_at(source, listener_xyz):
        """
        Inverse-square falloff.
        """
        if not source.active:
            return 0.0

        sx, sy, sz = source.position
        lx, ly, lz = listener_xyz

        dx = lx - sx
        dy = ly - sy
        dz = lz - sz

        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        if distance < 1.0:
            distance = 1.0  # prevent blow-up

        return source.base_volume / (distance ** 2)