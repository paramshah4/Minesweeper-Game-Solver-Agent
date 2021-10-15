from src.create_maze import create_maze

dimension = 5
density = 0.2

maze = create_maze(dimension, "original", density)


for i in range(0, dimension):
    for j in range(0, dimension):
        print(str(maze[i][j].state) + " ", end=" ")
    print("\n")
print("\n\n\n")

for i in range(0, dimension):
    for j in range(0, dimension):
        print(str(maze[i][j].cx) + " ", end=" ")
    print("\n")
print("\n\n\n")

for i in range(0, dimension):
    for j in range(0, dimension):
        print(str(maze[i][j].bx) + " ", end=" ")
    print("\n")
print("\n\n\n")

for i in range(0, dimension):
    for j in range(0, dimension):
        print(str(maze[i][j].ex) + " ", end=" ")
    print("\n")
print("\n\n\n")

for i in range(0, dimension):
    for j in range(0, dimension):
        print(str(maze[i][j].hx) + " ", end=" ")
    print("\n")
