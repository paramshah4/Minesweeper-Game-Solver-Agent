from helper.calculate_state import cal_state
from helper.calculate_hn import cal_hn
from helper.calculate_gn import cal_gn
from helper.constants import INF
from helper.calculate_nx import cal_nx
from helper.calculate_cx import cal_cx
from helper.calculate_bx import cal_bx
from helper.calculate_ex import cal_ex
from helper.calculate_hx import cal_hx
from helper.calculate_visited import cal_visited
from helper.calculate_fn import cal_fn


class Cell:
    """
    Defining the structure of each cell in the maze.
    """
    def __init__(self, state, parent, fn, gn, hn, nx, visited, cx, bx, ex, hx, hidden):
        """

        :param state: state of the cell(blocked-0 or unblocked-1)
        :param parent: indices of parent cell
        :param fn: f(n) value
        :param gn: g(n) value
        :param hn: h(n) value
        :param nx: number of neighbors
        :param visited: visited or not (type boolean)
        :param cx: number of neighbors sensed to be blocked
        :param bx: number of neighbors known to be blocked
        :param ex: number of neighbors known to be empty
        :param hx: number of hidden (unconfirmed whether empty or blocked)
        """
        self.state = state                          # 0 for unblock, 1 for block and -1 for unconfirmed
        self.parent = parent
        self.fn = fn
        self.gn = gn
        self.hn = hn
        self.nx = nx
        self.visited = visited                     # boolean value
        self.cx = cx
        self.bx = bx
        self.ex = ex
        self.hx = hx
        self.hidden = hidden


def set_attributes(maze, dimension, density, type_of_maze):
    """
    :param maze: the maze for which the attributes are to be set
    :param dimension: the dimension of maze
    :param type_of_maze: tells for which type of maze(the original with all information or the undiscovered one)
                        the attributes are to be set
    :param density: Probability  with which a cell is blocked.
    :return: Nothing as the maze objects attributes will directly get changed.
    """
    for i in range(0, dimension):
        for j in range(0, dimension):
            if (i == 0) and (j == 0):
                maze[i][j].state = 0
                maze[i][j].gn = cal_gn(i, j, dimension, maze, type_of_maze)
                maze[i][j].hn = cal_hn(i, j, dimension)
                maze[i][j].fn = cal_fn(maze, i, j, type_of_maze)
                maze[i][j].parent = (999, 999)                     # parent of start cell is (999,999)

            elif (i == dimension - 1) and (j == dimension - 1):
                maze[i][j].state = 0
                maze[i][j].gn = cal_gn(i, j, dimension, maze, type_of_maze)
                maze[i][j].hn = cal_hn(i, j, dimension)  # n-dim -> n+n
                maze[i][j].fn = cal_fn(maze, i, j, type_of_maze)
                maze[i][j].parent = (-1, -1)

            else:
                maze[i][j].state = cal_state(density, type_of_maze)
                maze[i][j].gn = cal_gn(i, j, dimension, maze, type_of_maze)
                maze[i][j].hn = cal_hn(i, j, dimension)
                maze[i][j].fn = cal_fn(maze, i, j, type_of_maze)
                maze[i][j].parent = (-1, -1)

    for i in range(0, dimension):
        for j in range(0, dimension):
            maze[i][j].nx = cal_nx(dimension, i, j)
            maze[i][j].cx = cal_cx(maze, dimension, i, j, type_of_maze)
            maze[i][j].bx = cal_bx(maze, dimension, i, j, type_of_maze)
            maze[i][j].ex = cal_ex(maze, dimension, i, j, type_of_maze)
            maze[i][j].hx = cal_hx(maze, i, j, type_of_maze)
            maze[i][j].visited = cal_visited(type_of_maze)


def create_maze(dimension, type_of_maze, density):
    """
    Function for creating a gridworld of dimension*dimension
    :param dimension: Dimension of maze.
    :param type_of_maze: tells which type of maze to create(the original with all information or the undiscovered one)
    :param density: Probability  with which a cell is blocked.
    :return: created maze.
    """

    maze = list()
    # making list of lists of objects of class Cell.
    for i in range(0, dimension):
        sub_maze = []
        for j in range(0, dimension):
            sub_maze.append(Cell(-1, (-1, -1), 0, 0, 0, 0, False, 0, 0, 0, 0, True))
        maze.append(sub_maze)

    set_attributes(maze, dimension, density, type_of_maze)

    return maze
