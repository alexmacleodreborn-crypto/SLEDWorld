import numpy as np

def coherence_gate(points_xy, grid_size: int = 32):
    """
    SandySquare-lite coherence:
    - Build occupancy grid from points.
    - Coherence increases when points cluster and persist.
    points_xy: list of (x, y) in grid coords [0..grid_size-1]
    Returns float in [0,1]
    """
    if not points_xy:
        return 0.0

    g = np.zeros((grid_size, grid_size), dtype=float)
    for (x, y) in points_xy:
        if 0 <= x < grid_size and 0 <= y < grid_size:
            g[int(y), int(x)] += 1.0

    total = float(g.sum())
    if total <= 0:
        return 0.0

    # normalized density
    p = g / total
    # entropy of distribution (lower entropy => more coherent)
    eps = 1e-12
    entropy = -float(np.sum(p * np.log(p + eps)))  # 0..log(N)
    max_entropy = np.log(grid_size * grid_size)
    entropy_norm = entropy / max_entropy if max_entropy > 0 else 1.0

    # coherence is inverse entropy, softened
    coherence = 1.0 - entropy_norm
    coherence = float(max(0.0, min(1.0, coherence)))
    return coherence