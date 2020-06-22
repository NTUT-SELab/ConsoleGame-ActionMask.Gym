def nearestPoint(pos):
    """
    Finds the nearest grid point to a position (discretizes).
    """
    (current_row, current_col) = pos

    grid_row = int(current_row + 0.5)
    grid_col = int(current_col + 0.5)
    return (grid_row, grid_col)


def manhattanDistance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
