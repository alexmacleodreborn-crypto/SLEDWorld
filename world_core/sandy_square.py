# world_core/sandys_square.py

import numpy as np

def square_from_points(points, size=32):
    """
    Create a binary grid from integer points [(y,x), ...].
    """
    grid = np.zeros((size, size), dtype=np.uint8)
    for (y, x) in points:
        if 0 <= y < size and 0 <= x < size:
            grid[y, x] = 1
    return grid

def crowding_score(grid: np.ndarray) -> float:
    """
    Measures local crowding: average of 3x3 neighborhood sums where occupied.
    Higher means clustered structure vs noise.
    """
    if grid.size == 0:
        return 0.0

    g = grid.astype(np.float32)
    # pad and sum neighbors
    p = np.pad(g, 1)
    neigh = (
        p[0:-2, 0:-2] + p[0:-2, 1:-1] + p[0:-2, 2:] +
        p[1:-1, 0:-2] + p[1:-1, 1:-1] + p[1:-1, 2:] +
        p[2:,   0:-2] + p[2:,   1:-1] + p[2:,   2:]
    )
    occupied = (g > 0)
    if occupied.sum() == 0:
        return 0.0
    return float(neigh[occupied].mean() / 9.0)  # 0..1

def coherence_gate(points, size=32) -> float:
    """
    SandySquare coherence in [0,1]:
    - higher when points form stable clusters (structure)
    - lower when points are scattered (noise)
    """
    grid = square_from_points(points, size=size)
    return max(0.0, min(1.0, crowding_score(grid)))