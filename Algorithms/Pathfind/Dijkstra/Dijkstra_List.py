"""
This code implements an adaptable version of Dijkstra's pathfinding algorithm
"""

class Dijkstra_Node():
    """A node class for Dijkstra's pathfinding algorithm"""

    def __init__(self, idf, previous=None):
        self.idf = idf
        self.previous = previous

        self.cost = 0

    def __eq__(self, other):
        return self.idf == other.idf

    def __lt__(self, other):
        return self.cost < other.cost


def Dijkstra(start, end, adjacency_func, cost_func):
    """
    Returns a two items tuple according to the format:
        ( list of tuples as a path , path total cost )
    Including the start and the end nodes

    Arguments:
        - start
            start node idf
        - end
            end node idf
        - adjacency_func(node_idf)
            function that yield each adjacent node idf
        - cost_func(node1_idf, node2_idf)
            function that returns the cost from node1 to node2
    """

    # Create start and end node
    start_node = Dijkstra_Node(start)
    start_node.cost = cost_func(None, start)
    end_node = Dijkstra_Node(end)

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Add the start node
    open_list.append(start_node)

    # Loop until find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = min(open_list)

        # Pop current off open list, add to closed list
        open_list.remove(current_node)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.idf)
                current = current.previous
            return (path[::-1],current_node.cost) # Return reversed path

        # Generate new nodes
        for new_idf in adjacency_func(current_node.idf):

            # Create new node
            new_node = Dijkstra_Node(new_idf, current_node)

            # New node is on the closed list
            if new_node in closed_list:
                continue
            
            # Set the new node cost
            new_node.cost = current_node.cost + cost_func(current_node.idf, new_node.idf)

            # New node is already in the open list
            for open_node in open_list:
                if new_node == open_node and new_node.cost >= open_node.cost:
                    break
            else:
                # Add the new node to the open list
                open_list.append(new_node)