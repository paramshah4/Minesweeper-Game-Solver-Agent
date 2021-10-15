# importing necessary requirements
from src.create_maze import create_maze
from src.AStar import astar  # importing A* to use during planning phase


def exampleInferenceAgent(MAZE, DIM, x, y):
    """
    This is the function of Repeated A*. The agent uses this to plan the path and actually traverse on it.
    :param MAZE: original maze with all full information used by agent when it walks down the path.
    :param DIM: the dimension of maze.
    :param x: i value in (i,j) denoting start cell (0,0)
    :param y: j value in (i,j) denoting start cell (0,0)
    :return: path planned, blocked-set list, nodes processed
    """
    block_count = 0
    dimension = DIM
    # maze with full information.
    og_maze = MAZE
    # create a new maze with density 0 as no blocked cells and update it when agent gets knowledge of the cells.
    new_maze = create_maze(dimension, "new", 0)
    # new_path is the list which contains the final trajectory of agent.
    new_path = list()
    # fist call to A* to plan the initial path.
    path, blocked_cell, cells_popped = astar(new_maze, dimension, x, y)

    # total_cells_popped keeps track of all the cells popped from the fringe by A*.
    total_cells_popped = cells_popped
    # loop until path returned by A* is [-1] which means no path is available, till goal is reached, or path list
    # becomes empty denoting no node from start to goal.

    while path:
        # z contains the indices of the path at 0 position.
        for z in path:
            updateState = -1
            currState = -1
            # checking if path returned by A* is [-1] or not
            if path == [-1]:
                return [-1], total_cells_popped
            # reaching here means path has values in it which the agent will now process and traverse accordingly.
            (i1, j1) = z
            # check if goal is reached. If condition met then append the goal node indices to the new_path and assess
            # the neighbouring cells in FOV(field of view) and update the environment. Also return the trajectory
            # nodes popped off(nodes processed)
            if (i1, j1) == (DIM - 1, DIM - 1):
                new_path.append((i1, j1))
                # neighbours = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                # for (X, Y) in neighbours:
                #     a = i1 + X
                #     b = j1 + Y
                #     if a + b > 0 and 0 <= a < dim1 and 0 <= b < dim1:
                #         new_maze[a][b].state = og_maze[a][b].state
                return block_count,new_path, total_cells_popped
            # if not goal then append it to new_path as agent walks on it. Also update the FOV during walking phase.
            else:
                if og_maze[i1][j1].state == 1:
                    block_count=block_count + 1
                    #new_maze[i1][j1].cx = og_maze[i1][j1].cx
                    new_maze[i1][j1].hidden = False
                    new_maze[i1][j1].state = og_maze[i1][j1].state
                    #updatingNeighbourValuesAndStates(new_maze, i1, j1, 1, -1, dimension)
                    updateNeigh(new_maze, i1, j1,dimension,path)
                    path.clear()
                    parentx, parenty = new_maze[i1][j1].parent
                    #print("Astar called for:" + str((parentx, parenty)))
                    path, blocked_cell, cells_popped = astar(new_maze, dimension,parentx, parenty)
                    new_path.pop()
                    total_cells_popped = total_cells_popped + cells_popped
                else:
                    new_maze[i1][j1].hidden = False
                    new_maze[i1][j1].state = og_maze[i1][j1].state
                    #currState = new_maze[i1][j1].state
                    new_maze[i1][j1].cx = og_maze[i1][j1].cx
                    new_path.append((i1, j1))
                    if updateNeigh(new_maze,i1,j1,dimension,path) is True:
                        #print("Astar called for:" + str((parentx, parenty)))
                        path, blocked_cell, cells_popped = astar(new_maze, dimension, i1, j1)
                        new_path.pop()
                        total_cells_popped = total_cells_popped + cells_popped
                    # if new_maze[i1][j1].hx == 0 and new_maze[i1][j1].state != 1:
                    #     continue
                    # elif new_maze[i1][j1].cx == new_maze[i1][j1].bx:
                    #     updateState = 0
                    # elif new_maze[i1][j1].ex == (new_maze[i1][j1].nx - new_maze[i1][j1].cx):
                    #     updateState = 1
                    #
                    # neighbours = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1),
                    #               (-1, 1)]  # for updating field of view
                    # for (X, Y) in neighbours:
                    #     a = i1 + X
                    #     b = j1 + Y
                    #     if a + b > 0 and 0 <= a < dimension and 0 <= b < dimension and new_maze[a][b].visited is False:
                    #         if currState == 1:
                    #             new_maze[a][b].bx += 1
                    #         else:
                    #             new_maze[a][b].ex += 1
                    #
                    #         new_maze[a][b].hx -= 1
                    #         if updateState != -1 and new_maze[a][b].hidden:
                    #             #print("before update the cell"+str((a,b))+"state is:"+str(new_maze[a][b].state))
                    #             new_maze[a][b].state = updateState
                    #             new_maze[a][b].hidden = False
                                #print("after update the cell" + str((a, b)) + "state is:" + str(new_maze[a][b].state))
                                #updatingNeighbours(new_maze, og_maze, a, b, updateState, dimension)
                                #updatingNeighbourValuesAndStates(new_maze, a, b, updateState, -1, dimension)


                # check if next cell in the path returned by A* is blocked or not. If it's blocked, then run the
                # planning phase by making a call to astar with the current cell the agent has walked on.
                # index = path.index((i1, j1)) + 1
                # (p, q) = path[index]

                # popping to avoid 2 entries of the same current cell the agent is on because we have already
                # appended it and the path from A* will also have the same start cell which will again append in
                # next iteration
                # new_path.pop()
    # return [-1] as trajectory because no path exits as all cells have been processed and goal is not met.
    return block_count,[-1], total_cells_popped


# def updatingNeighbours(new_maze, og_maze, i1, j1, currState, dimension):
#     neighbours = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]  # for updating field of view
#     for (X, Y) in neighbours:
#         a = i1 + X
#         b = j1 + Y
#         if a + b > 0 and 0 <= a < dimension and 0 <= b < dimension and new_maze[i1][j1].visited is False:
#             if currState == 1:
#                 new_maze[a][b].bx += 1
#             else:
#                 new_maze[a][b].ex += 1
#
#             new_maze[a][b].hx -= 1


def updateNeigh(new_maze, x, y,dimension,path):
    queue=[]
    blocked=False
    queue.append((x,y))
    while len(queue) > 0:
        updateState=-1
        flag=False
        i1,j1=queue.pop(0)
        currState=new_maze[i1][j1].state
        if new_maze[i1][j1].cx!=-1 and currState==0:
            if new_maze[i1][j1].hx == 0:
                updateState=-1
            elif new_maze[i1][j1].cx == new_maze[i1][j1].bx:
                updateState = 0
                flag=True
            elif new_maze[i1][j1].ex == (new_maze[i1][j1].nx - new_maze[i1][j1].cx):
                updateState = 1
                flag=True
        neighbours = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]  # for updating field of view
        if new_maze[i1][j1].visited is False or flag is True:
            for (X, Y) in neighbours:
                a = i1 + X
                b = j1 + Y
                if 0 <= a < dimension and 0 <= b < dimension:
                    if new_maze[i1][j1].visited is False:
                        if currState == 1:
                            new_maze[a][b].bx += 1
                        else:
                            new_maze[a][b].ex += 1

                        new_maze[a][b].hx -= 1

                    if new_maze[a][b].visited is True:
                        queue.append((a,b))
                    else:
                        if updateState != -1 and new_maze[a][b].hidden is True:
                            new_maze[a][b].state=updateState
                            new_maze[a][b].hidden = False
                            queue.append((a, b))
                            if updateState == 1 and (a,b) in path:
                                blocked=True

        new_maze[i1][j1].visited = True
        return blocked
# def updatingNeighbourValuesAndStates(new_maze, i1, j1, currState,updateState,dimension):
#     #print(str(i1 )+str(j1 ))
#     neighbours = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]  # for updating field of view
#     for (X, Y) in neighbours:
#         a = i1 + X
#         b = j1 + Y
#         if 0 <= a < dimension and 0 <= b < dimension:
#             if currState == 1:
#                 new_maze[a][b].bx += 1
#             else:
#                 new_maze[a][b].ex += 1
#
#             new_maze[a][b].hx -= 1
#
#             if new_maze[a][b].hidden is False:
#                 if new_maze[a][b].hx==0:
#                     continue
#                 elif new_maze[a][b].cx == new_maze[a][b].bx:
#                     updatingNeighbourValuesAndStates(new_maze,a,b,new_maze[a][b].state,0,dimension)
#                 elif new_maze[a][b].ex == (new_maze[a][b].nx - new_maze[a][b].cx):
#                     updatingNeighbourValuesAndStates(new_maze,a,b,new_maze[a][b].state,1,dimension)
#             else:
#                 if updateState != -1:
#                     new_maze[a][b].state=updateState
#                     new_maze[a][b].hidden=False



