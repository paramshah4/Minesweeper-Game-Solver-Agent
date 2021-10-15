from helper.constants import INF


def cal_gn(a, b, dimension, maze, type_of_maze):
    """

    :param a: x-coordinate of the cell
    :param b: y-coordinate of the cell
    :param dimension: dimension of maze
    :param maze: maze object
    :param type_of_maze: tells for which type of maze(the original with all information or the undiscovered one) the
                        g(n) value is to be set
    :return: Nothing as the maze objects attribute will directly get changed.
    """

    if type_of_maze == "original":
        if (a == 0) & (b == 0):
            return 0

        elif (a == dimension-1) & (b == dimension-1):
            return dimension+dimension-2

        else:
            if b == 0:
                return maze[a - 1][0].gn + 1
            else:
                return maze[a][b-1].gn + 1

    else:
        if (a == 0) & (b == 0):
            return 0
        else:
            return INF
