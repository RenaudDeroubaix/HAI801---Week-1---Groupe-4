import heapq
import matplotlib.pyplot as plt
import numpy as np
import time

class Node:
    def __init__(self, name, heuristic):
        self.name = name
        self.heuristic = heuristic
        self.rootDist = float('inf')  # distance par rapport a la racine du graphe
        self.nearestPathCost = float('inf')  # cout du chemin le plus court
        self.neighbor = {}  # voisinage (noeuds adjacents dans le graphe)
        self.parent = None  # noeud parent
        self.explored = False  # pour la visualisation

    def __lt__(self, other):
        return self.nearestPathCost < other.nearestPathCost

    def add_edge(self, neighbor, cost):
        self.neighbor[neighbor] = cost

def astar(graph, start, end, visualize=False):
    start_node = graph[start]
    start_node.rootDist = 0
    start_node.nearestPathCost = start_node.heuristic

    explore = []
    heapq.heappush(explore, start_node)
    frontiere = set()

    if visualize:
        fig, ax = plt.subplots()

    while explore:
        current_node = heapq.heappop(explore)
        current_node.explored = True
        frontiere.add(current_node)

        if visualize:
            plt.cla()
            for node in graph.values():
                for neighbor, cost in node.neighbor.items():
                    if node.explored and graph[neighbor].explored:
                        plt.plot([node.name, neighbor], [node.heuristic, graph[neighbor].heuristic], 'r-')
                    else:
                        plt.plot([node.name, neighbor], [node.heuristic, graph[neighbor].heuristic], 'k-')

            for node in frontiere:
                plt.plot(node.name, node.heuristic, 'bo')
            plt.pause(0.5)

        if current_node.name == end:
            path = []
            while current_node:
                path.append(current_node.name)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        for adj, cost in current_node.neighbor.items():
            child_node = graph[adj]
            if child_node in frontiere:
                continue

            tentative_g_score = current_node.rootDist + cost

            if tentative_g_score < child_node.rootDist:
                child_node.parent = current_node
                child_node.rootDist = tentative_g_score
                child_node.nearestPathCost = tentative_g_score + child_node.heuristic

                if child_node not in explore:
                    heapq.heappush(explore, child_node)

    return None

start_time = time.time()

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

end_time = time.time()
elapsed_time = end_time - start_time

print("Temps d'exécution :", elapsed_time, "secondes")

path = astar(nodes, 'A', 'H', visualize=True)
print("Path found by A*:", path)

plt.show()  # Show the final graph