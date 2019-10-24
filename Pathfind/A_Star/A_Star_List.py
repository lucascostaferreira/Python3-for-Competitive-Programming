"""
This code applies A* algorithm to a given weights matrix (0 for impassable)
"""

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, position, previous=None):
        self.position = position
        self.previous = previous

        self.g = 0
        self.h = 0

    @property
    def f(self):
        return self.g + self.h

    def __eq__(self, other):
        return self.position == other.position


def A_Star(start, end, adjacency_func, cost_func, heuristic_func):
    """
    Returns a two items tuple according to the format:
        ( list of tuples as a path , path total cost )
    Including the start and the end nodes

    Arguments:
        - start
            start node position
        - end
            end node position
        - adjacency_func(node)
            function that yield each adjacent position
        - cost_func(node1, node2)
            function that returns the cost from node1 to node2
        - heuristic_func(node1, node2)
            function that returns the heuristcs from node1 to node2
    """

    # Create start and end node
    start_node = Node(start)
    start_node.g = cost_func(None, start)
    end_node = Node(end)

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.previous
            return (path[::-1],current_node.g) # Return reversed path

        # Generate new nodes
        for new_position in adjacency_func(current_node.position):

            # Create new node
            new_node = Node(new_position, current_node)

            # New node is on the closed list
            if new_node in closed_list:
                continue
            
            # Set the new node cost
            new_node.g = current_node.g + cost_func(current_node.position, new_node.position)

            # New node is already in the open list
            for open_node in open_list:
                if new_node == open_node and new_node.g > open_node.g:
                    break
            else:
                # Set the new node heuristic
                new_node.h = heuristic_func(new_node.position, end_node.position)
                
                # Add the new node to the open list
                open_list.append(new_node)


import os
os.system('cls')

print("Enter the weights matrix (0 for impassable, EOF to stop entering):\n")
maze = []
while True:
    try:
        maze.append(list(map( int,input().split() )))
    except:
        break

start = tuple(map( int,input("Start: ").split() ))
end   = tuple(map( int,input("End:   ").split() ))

def adjacency(n1_pos):
    l0, c0 = n1_pos
    for l,c in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        try:
            if (l0+l >= 0) and (c0+c >= 0) and (maze[l0+l][c0+c] != 0):
                yield (l0+l,c0+c)
        except:
            continue

cost     = lambda n1_pos, n2_pos: maze[n2_pos[0]][n2_pos[1]]
distance = lambda n1_pos, n2_pos: (((n1_pos[0] - n2_pos[0]) ** 2) + ((n1_pos[1] - n2_pos[1]) ** 2)) ** (1/2)

path, weight = A_Star(start, end, adjacency, cost, distance)

maze[start[0]][start[1]] = '>'
maze[end[0]][end[1]]     = '>'

for x,y in path[1:]:
    os.system('cls')
    for line in maze:
        print( " ".join([ str(c) for c in line ]) )
    input()
    maze[x][y] = '.'

print("Path =",path)
print("Weight =",weight)

"""
1 1 0 0 1 0
1 0 1 0 2 1
1 3 1 2 1 1
2 1 1 0 2 1
0 1 2 0 2 1
1 1 1 2 1 1
"""