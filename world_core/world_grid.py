import numpy as np

class WorldGrid:
    """
    Registers objects and can render a coarse occupancy map.
    """
    def __init__(self):
        self.objects = []

    def register(self, obj):
        self.objects.append(obj)

    def render_occupancy(self, size: int = 64):
        # Find overall bounds from registered objects
        mins = []
        maxs = []
        for o in self.objects:
            if getattr(o, "bounds", None):
                (min_x, min_y, _), (max_x, max_y, _) = o.bounds
                mins.append((min_x, min_y))
                maxs.append((max_x, max_y))
            else:
                x, y, _ = o.position
                mins.append((x, y))
                maxs.append((x, y))

        if not mins:
            return np.zeros((size, size), dtype=float)

        min_x = min(p[0] for p in mins)
        min_y = min(p[1] for p in mins)
        max_x = max(p[0] for p in maxs)
        max_y = max(p[1] for p in maxs)

        w = max(1.0, max_x - min_x)
        h = max(1.0, max_y - min_y)

        grid = np.zeros((size, size), dtype=float)

        for o in self.objects:
            if getattr(o, "bounds", None):
                (bx0, by0, _), (bx1, by1, _) = o.bounds
            else:
                x, y, _ = o.position
                bx0, by0, bx1, by1 = x, y, x, y

            x0 = int(((bx0 - min_x) / w) * (size - 1))
            x1 = int(((bx1 - min_x) / w) * (size - 1))
            y0 = int(((by0 - min_y) / h) * (size - 1))
            y1 = int(((by1 - min_y) / h) * (size - 1))

            x0, x1 = sorted((max(0, x0), min(size-1, x1)))
            y0, y1 = sorted((max(0, y0), min(size-1, y1)))

            grid[y0:y1+1, x0:x1+1] = 1.0

        return grid