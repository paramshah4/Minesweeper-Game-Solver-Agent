from src.create_maze import create_maze
from src.AStar import astar
from src.Repeated_AStar import repeated_forward_astar
from src.ExampleInferenceAgent import exampleInferenceAgent
from src.Repeated_AStar_Limited_FOV import repeated_forward_astar_limited_fov
from src.Inference4thAgent import inferenceAgentModified


dimension =101
density = 0.25
p_list = list()
x_axis = list()
y_axis = list()

maze = create_maze(dimension, "original", density)

for i in range(0, dimension):
    for j in range(0, dimension):
        print(str(maze[i][j].state) + " ", end=" ")
    print("\n")
print("\n\n\n")



path_from_astar, blocked_cell, nodes_traversed = astar(maze, dimension, 0, 0)
if path_from_astar == [-1]:
    print("No path from start to goal")
else:
    print("Path:" + str(nodes_traversed))


path_from_astar, nodes_traversed = repeated_forward_astar_limited_fov(maze, dimension, 0, 0)
if path_from_astar == [-1]:
    print("No path from start to goal")
else:
    print("Path:" +  "nodes traversed:"+ str(nodes_traversed))
#
path_from_astar, nodes_traversed = repeated_forward_astar(maze, dimension, 0, 0)
if path_from_astar == [-1]:
    print("No path from start to goal")
else:
    print("Path:" + "nodes traversed:"+ str(nodes_traversed))

blocked_count,path_from_repeated_astar, cells_processed = exampleInferenceAgent(maze, dimension, 0, 0)
if path_from_repeated_astar == [-1]:
    print("No path from start to goal")
else:
    print("Blocked Count: " + str(blocked_count))
    print("Traversed Path:" + "cell processed" + str(cells_processed))



print("*"* 50)
print("*"* 50)


blocked_count,path_from_repeated_astar, cells_processed = inferenceAgentModified(maze, dimension, 0, 0)
if path_from_repeated_astar == [-1]:
    print("No path from start to goal")
else:
    print("Blocked Count: "+ str(blocked_count))
    print("Traversed Path:" + "cell processed" + str(cells_processed))
