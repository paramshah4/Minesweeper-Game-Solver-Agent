def cal_ex(maze, dimension, a, b, type_of_maze):
    if type_of_maze == "original":
        count = 0
        neighbors = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        for (i, j) in neighbors:
            x = a + i
            y = b + j
            if 0 <= x <= (dimension - 1) and 0 <= y <= (dimension - 1):
                if maze[x][y].state == 0:                    # or maze[x][y].state == 10 or maze[x][y].state == 100:
                    count = count + 1
        return count

    else:
        return 0
