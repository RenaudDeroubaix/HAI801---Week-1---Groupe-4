import heapq
import matplotlib.pyplot as plt
import numpy as np

class Node:
    def __init__(self, name, heuristic):
        self.name = name
        self.heuristic = heuristic
        self.g = float('inf')  # Distance from start node
        self.f = float('inf')  # Total estimated cost of the cheapest solution through this node
        self.adjacent = {}  # Adjacent nodes and their costs
        self.parent = None  # Parent node in the path

    def __lt__(self, other):
        return self.f < other.f

    def add_edge(self, neighbor, cost):
        self.adjacent[neighbor] = cost

def astar(graph, start, end):
    start_node = graph[start]
    start_node.g = 0
    start_node.f = start_node.heuristic

    open_list = []
    heapq.heappush(open_list, start_node)
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node)

        if current_node.name == end:
            path = []
            while current_node:
                path.append(current_node.name)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        
        for adj, cost in current_node.adjacent.items():
            child_node = graph[adj]
            if child_node in closed_set:
                continue

            tentative_g_score = current_node.g + cost

            if tentative_g_score < child_node.g:
                child_node.parent = current_node
                child_node.g = tentative_g_score
                child_node.f = tentative_g_score + child_node.heuristic

                if child_node not in open_list:
                    heapq.heappush(open_list, child_node)

    return None

nodes = {}
heuristics = {'A': 9, 'B': 3, 'C': 5, 'D': 6, 'E': 8, 'F': 4, 'G': 2, 'H': 0}
for node, h_val in heuristics.items():
    nodes[node] = Node(node, h_val)

edges = {
    ('A', 'B', 2),
    ('A', 'C', 10),
    ('A', 'D', 3),
    ('B', 'E', 8),
    ('C', 'D', 2),
    ('C', 'G', 2),
    ('D', 'C', 2),
    ('D', 'F', 4),
    ('E', 'H', 10),
    ('F', 'E', 5),
    ('F', 'G', 5),
    ('G', 'H', 1)
}

for edge in edges:
    nodes[edge[0]].add_edge(edge[1], edge[2])

path = astar(nodes, 'A', 'H')
print("Path found by A*:", path)
