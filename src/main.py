from src.create_maze import create_maze
from src.AStar import astar
from src.Repeated_AStar import repeated_forward_astar

dimension = 5
density = 0.1
p_list = list()
x_axis = list()
y_axis = list()

maze = create_maze(dimension, "original", density)

path_from_astar, blocked_cell, nodes_traversed = astar(maze, dimension, 0, 0)
if path_from_astar == [-1]:
    print("No path from start to goal")
else:
    print("Path:" + str(path_from_astar))

path_from_repeated_astar, cells_processed = repeated_forward_astar(maze, dimension, 0, 0)
if path_from_repeated_astar == [-1]:
    print("No path from start to goal")
else:
    print("Traversed Path:" + str(path_from_repeated_astar))



