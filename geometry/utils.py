def point_in_polygon(point, polygon):
    """
    Ray casting algorithm for point-in-polygon test.
    """

    x, y = point
    inside = False

    n = len(polygon)
    j = n - 1

    for i in range(n):

        xi, yi = polygon[i]
        xj, yj = polygon[j]

        intersect = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi
        )

        if intersect:
            inside = not inside

        j = i

    return inside