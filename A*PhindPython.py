import heapq

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = {edge[0]: [(edge[1], edge[2])] for edge in edges}

    def neighbors(self, node):
        return self.edges[node]

    def cost(self, from_node, to_node):
        for neighbor, cost in self.neighbors(from_node):
            if neighbor == to_node:
                return cost

def heuristic(graph, node):
    return graph.nodes[node]

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def a_star_search(graph, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for next_node, cost in graph.neighbors(current):
            new_cost = cost_so_far[current] + cost
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(graph, next_node)
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current

    return came_from, cost_so_far

nodes = {'A': 9, 'B': 3, 'C': 5, 'D': 6, 'E': 8, 'F': 4, 'G': 2, 'H': 0}
edges = [['A', 'B', 2], ['A', 'C', 10], ['A', 'D', 3], ['B', 'E', 8], ['C', 'D', 2], ['C', 'G', 2], ['D', 'C', 2], ['D', 'F', 4], ['E', 'H', 10], ['F', 'E', 5], ['F', 'G', 5], ['G', 'H', 1]]
graph = Graph(nodes, edges)
start, goal = 'A', 'H'
came_from, cost_so_far = a_star_search(graph, start, goal)
path = reconstruct_path(came_from, start, goal)
print('Chemin trouvé : ', path)
