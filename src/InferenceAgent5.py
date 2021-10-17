# importing necessary requirements
from src.create_maze import create_maze
from src.AStar import astar  # importing A* to use during planning phase
from src.modifiedAstarfifth import astarModified
kb = []  # knowledgebase
kb_queue = []  # knowledgebase queue


neighbours = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
def inferenceAgentModifiedfifth(MAZE, DIM, x, y):
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
    path, blocked_cell, cells_popped = astarModified(new_maze, dimension, x, y)

    # total_cells_popped keeps track of all the cells popped from the fringe by A*.
    total_cells_popped = cells_popped
    # loop until path returned by A* is [-1] which means no path is available, till goal is reached, or path list
    # becomes empty denoting no node from start to goal.




    while path:

        for z in path:

            if path == [-1]:
                return [-1], total_cells_popped

            (i1, j1) = z

            if (i1, j1) == (DIM - 1, DIM - 1):
                new_path.append((i1, j1))
                print()
                return block_count,new_path, total_cells_popped

            else:
                if og_maze[i1][j1].state == 1:
                    block_count=block_count+1
                    new_maze[i1][j1].cx = og_maze[i1][j1].cx
                    new_maze[i1][j1].hidden = False
                    new_maze[i1][j1].state = og_maze[i1][j1].state
                    updateNeighbour(new_maze, i1, j1, dimension, 1)
                    #generateEquations(new_maze, og_maze, dimension, i1, j1)
                    path.clear()
                    parentx, parenty = new_maze[i1][j1].parent
                    path, blocked_cell, cells_popped = astarModified(new_maze, dimension, x, y)
                    new_path.pop()
                    total_cells_popped = total_cells_popped + cells_popped
                else:
                    new_maze[i1][j1].hidden = False
                    new_maze[i1][j1].state = og_maze[i1][j1].state
                    updateNeighbour(new_maze, i1, j1, dimension, new_maze[i1][j1].state)
                    new_maze[i1][j1].cx = og_maze[i1][j1].cx
                    new_path.append((i1, j1))
                    generateEquations(new_maze, og_maze, dimension, i1, j1)
    return block_count,[-1], total_cells_popped



def generateEquations(new_maze, old_maze, dimension, x, y):
    equation = []
    eq_parts = set()
    difference_set = set()
    isSubsetFlag = False
    addKBFlag = False
    tempsum = 0
    if new_maze[x][y].visited is False:
        for (X, Y) in neighbours:
            a = x + X
            b = y + Y
            if 0 <= a < dimension and 0 <= b < dimension:
                if new_maze[a][b].hidden is True:
                    eq_parts.add((a, b))
                    tempsum = tempsum + old_maze[a][b].state

        if len(eq_parts) == 0:
            return
        equation.append(eq_parts)
        equation.append(tempsum)
        # print(equation)
        kb_queue.append(equation)
        while (len(kb_queue) > 0):
            # print(kb_queue)
            curr_eq = kb_queue.pop(0)
            # print(curr_eq)
            # print(kb)
            curr_eq = updateCurrentEquation(curr_eq, new_maze, old_maze)
            if (curr_eq[1] == -1):
                return
            # print(curr_eq)
            if checkisSolvable(new_maze, curr_eq,dimension) is True:
                # print("Solvable")
                updateKnowledgeBase(new_maze)
                # print("KB is Solvable:" + str(kb))
                continue
            # print("KB: " + str(kb))
            # new_list=kb
            for kb_eq in kb:
                # print("inside loop")
                new_eq = []
                if curr_eq[0].issubset(kb_eq[0]) or kb_eq[0].issubset(curr_eq[0]):
                    # print("Is subset")
                    # print(curr_eq)
                    # print(kb_eq)
                    isSubsetFlag = True
                    if (len(curr_eq[0]) > len(kb_eq[0])):
                        # print("kb is smaller")
                        new_set = curr_eq[0].difference(kb_eq[0])
                        diff_set_val = curr_eq[1] - kb_eq[1]
                        new_eq.append(new_set)
                        new_eq.append(diff_set_val)
                        if len(new_set) != 0:
                            # print("NEW SET"+ str(new_eq))
                            kb_queue.append(new_eq)
                    elif (len(curr_eq[0]) < len(kb_eq[0])):
                        # print("kb is greater")
                        new_set = kb_eq[0].difference(curr_eq[0])
                        diff_set_val = kb_eq[1] - curr_eq[1]
                        new_eq.append(new_set)
                        new_eq.append(diff_set_val)
                        if len(new_set) != 0:
                            if (new_set) == 1:
                                kb_queue.insert(0, new_eq)
                            else:
                                # print("KB IS GREATER SET"+ str(kb_eq))
                                kb_queue.append(new_eq)
                        kb.remove(kb_eq)
                        addKBFlag = True

            # kb = list(filter(([set(),0]).__ne__, kb))
            if isSubsetFlag is False or addKBFlag is True:
                if (len(curr_eq[0])) != 0:
                    # print("NOWWW INSIDE")
                    # print(curr_eq)
                    kb.append(curr_eq)
                    # print(kb)

            setDifference(curr_eq, new_maze, old_maze,dimension)


def setDifference(curr_eq, new_maze, old_maze,dimension):
    for eq in kb:
        new_set = set()
        new_negative_set = set()
        #print(curr_eq)
        #print(eq)
        if eq[1] > curr_eq[1]:
            # print("greater")
            new_set = eq[0].difference(curr_eq[0])
            new_set_val = eq[1] - curr_eq[1]
            if len(new_set) == new_set_val:
                #print("update greater")
                # print(new_set)
                for coord in new_set:
                    if new_maze[coord[0]][coord[1]].hidden is True:
                        # if old_maze[coord[0]][coord[1]].state != 1:
                        #     print(curr_eq)
                        #     print(eq)
                        #     print(new_set)
                        new_maze[coord[0]][coord[1]].state = 1
                        new_maze[coord[0]][coord[1]].hidden = False
                        updateNeighbour(new_maze, coord[0], coord[1], dimension, 1)
                new_negative_set = curr_eq[0].difference(eq[0])
                for coord in new_negative_set:
                    if new_maze[coord[0]][coord[1]].hidden is True:
                        # if old_maze[coord[0]][coord[1]].state != 0:
                        #     print(curr_eq)
                        #     print(eq)
                        #     print(new_negative_set)
                        new_maze[coord[0]][coord[1]].state =0
                        new_maze[coord[0]][coord[1]].hidden = False
                        updateNeighbour(new_maze, coord[0], coord[1], dimension, 0)

        elif eq[1] == curr_eq[1]:
            continue
        else:
            #print("lower")
            new_set = curr_eq[0].difference(eq[0])
            new_set_val = curr_eq[1] - eq[1]
            if len(new_set) == new_set_val:
                #print("update lower")
                # print(new_set)
                for coord in new_set:
                    if new_maze[coord[0]][coord[1]].hidden is True:
                        # print(coord)
                        # print(old_maze[coord[0]][coord[1]].state)
                        # if old_maze[coord[0]][coord[1]].state != 1:
                        #     print(curr_eq)
                        #     print(eq)
                        #     print(new_set)
                        new_maze[coord[0]][coord[1]].state = 1
                        new_maze[coord[0]][coord[1]].hidden = False
                        updateNeighbour(new_maze, coord[0], coord[1], dimension, 1)
                new_negative_set = eq[0].difference(curr_eq[0])
                for coord in new_negative_set:
                    # print(coord)
                    # print(old_maze[coord[0]][coord[1]].state)
                    if new_maze[coord[0]][coord[1]].hidden is True:
                        # if old_maze[coord[0]][coord[1]].state != 0:
                        #     print(curr_eq)
                        #     print(eq)
                        #     print(new_negative_set)
                        new_maze[coord[0]][coord[1]].state = 0
                        new_maze[coord[0]][coord[1]].hidden = False
                        updateNeighbour(new_maze, coord[0], coord[1], dimension, 0)
        #print("*" * 20)


def checkisSolvable(new_maze, curr_eq,dimension):
    flag = False
    if len(curr_eq[0]) == curr_eq[1]:
        for coord in curr_eq[0]:
            new_maze[coord[0]][coord[1]].state = 1
            new_maze[coord[0]][coord[1]].hidden = False
            updateNeighbour(new_maze, coord[0], coord[1],dimension,1)
        flag = True
    elif curr_eq[1] == 0:
        for coord in curr_eq[0]:
            new_maze[coord[0]][coord[1]].state = 0
            new_maze[coord[0]][coord[1]].hidden = False
            updateNeighbour(new_maze, coord[0], coord[1], dimension, 0)
        flag = True
    return flag


def updateKnowledgeBase(new_maze):
    new_list = kb
    updateflag = False
    for eq in new_list:
        new_set = set()
        new_equation = []
        new_set_val = eq[1]
        for coord in eq[0]:
            if new_maze[coord[0]][coord[1]].hidden is False:
                updateflag = True
                new_set_val = new_set_val - new_maze[coord[0]][coord[1]].state
            else:
                new_set.add(coord)

        if updateflag is False:
            continue
        else:
            new_equation.append(new_set)
            new_equation.append(new_set_val)
            kb_queue.append(new_equation)
            kb.remove(eq)


def updateCurrentEquation(curr_eq, new_maze, og_maze):
    new_equation = []
    new_set = set()
    new_set_val = 0
    for coord in curr_eq[0]:
        if new_maze[coord[0]][coord[1]].hidden is True:
            new_set.add(coord)
            new_set_val = new_set_val + og_maze[coord[0]][coord[1]].state

    if len(new_set) == 0:
        new_set_val = -1
        new_set = curr_eq[0]
    new_equation.append(new_set)
    new_equation.append(new_set_val)
    return new_equation









def updateNeighbour(new_maze, i1, j1,dimension,currState):
    if new_maze[i1][j1].neighbor_updated is False:
        for (X, Y) in neighbours:
                a = i1 + X
                b = j1 + Y
                if 0 <= a < dimension and 0 <= b < dimension:
                        if currState == 1:
                            new_maze[a][b].bx += 1
                        else:
                            new_maze[a][b].ex += 1

                        new_maze[a][b].hx -= 1
                        new_maze[a][b].probablity_blocked.add((i1,j1))
        new_maze[i1][j1].neighbor_updated=True
    return






