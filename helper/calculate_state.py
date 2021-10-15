import random


def cal_state(density, type_of_maze):
    """
    Used for setting state of cells in maze.
    :param density: Probability  with which a cell is blocked.
    :param type_of_maze: tells for which type of maze(the original with all information or the undiscovered one) the
                        cell state value is to be set
    :return: state of cell(blocked, unblocked)
    """

    if type_of_maze == "original":
        r = random.uniform(0, 1)  # generate a random floating decimal between 0 and 1
        if r <= density:
            return 1  # 1 for blocked state
        else:
            return 0  # 0 for unblocked state

    else:
        return 0  # all unblocked for undiscovered maze
