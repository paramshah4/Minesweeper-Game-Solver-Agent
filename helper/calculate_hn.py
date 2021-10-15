def cal_hn(a, b, dimension):
    """
    This is same for both original and undiscovered cells and sets h(n) value according to Manhattan distance.
    :param a: x-coordinate of the cell
    :param b: y-coordinate of the cell
    :param dimension: dimension of maze
    :return: Nothing as the maze objects attribute will directly get changed.
    """

    return abs(a-(dimension-1))+abs(b-(dimension-1))
