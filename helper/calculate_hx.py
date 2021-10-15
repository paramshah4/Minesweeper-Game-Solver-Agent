def cal_hx(maze, a, b, type_of_maze):
    if type_of_maze == "original":
        return 0

    else:
        return maze[a][b].nx
