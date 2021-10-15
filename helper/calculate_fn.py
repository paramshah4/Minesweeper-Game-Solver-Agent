from helper.constants import INF


def cal_fn(maze, a, b, type_of_maze):
    if type_of_maze == "original":
        return maze[a][b].gn + maze[a][b].hn

    else:
        return INF