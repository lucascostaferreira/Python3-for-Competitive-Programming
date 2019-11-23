"""
This code implements an adaptable version of A* pathfinding algorithm
"""

from heapq import heappush, heappop

class A_Star_Node():
    """A node class for A* pathfinding algorithm"""

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

    def __lt__(self, other):
        return self.f < other.f


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
        - adjacency_func(node_pos)
            function that yield each adjacent position
        - cost_func(node1_pos, node2_pos)
            function that returns the cost from node1 to node2
        - heuristic_func(node1_pos, node2_pos)
            function that returns the heuristcs from node1 to node2
    """

    # Create start and end node
    start_node = A_Star_Node(start)
    start_node.g = cost_func(None, start)
    end_node = A_Star_Node(end)

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Add the start node
    heappush(open_list, start_node)

    # Loop until find the end
    while len(open_list) > 0:

        # Get the current node, pop current off open list, add to closed list
        current_node = heappop(open_list)
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
            new_node = A_Star_Node(new_position, current_node)

            # New node is on the closed list
            if new_node in closed_list:
                continue
            
            # Set the new node cost
            new_node.g = current_node.g + cost_func(current_node.position, new_node.position)

            # New node is already in the open list
            for open_node in open_list:
                if new_node == open_node and new_node.g >= open_node.g:
                    break
            else:
                # Set the new node heuristic
                new_node.h = heuristic_func(new_node.position, end_node.position)
                
                # Add the new node to the open list
                heappush(open_list, new_node)