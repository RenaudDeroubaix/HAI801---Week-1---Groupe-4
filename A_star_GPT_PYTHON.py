import heapq

def astar(graph, start, goal):
    open_set = [(0, start)]
    closed_set = set()
    g_scores = {node: float('infinity') for node in graph}
    g_scores[start] = 0
    f_scores = {node: float('infinity') for node in graph}
    f_scores[start] = heuristic(start, goal)

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = reconstruct_path(came_from, goal)
            return path

        closed_set.add(current)

        for neighbor, cost in graph[current]:
            if neighbor in closed_set:
                continue

            tentative_g_score = g_scores[current] + cost

            if tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                f_scores[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                if neighbor not in [node[1] for node in open_set]:
                    heapq.heappush(open_set, (f_scores[neighbor], neighbor))

def heuristic(node, goal):
    return nodes[goal]

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    return path[::-1]

# Données du graphe
nodes = { 'A': 9, 'B': 3, 'C': 5, 'D': 6, 'E': 8, 'F': 4, 'G': 2, 'H': 0 }
edges = [
    ['A', 'B', 2],
    ['A', 'C', 10],
    ['A', 'D', 3],
    ['B', 'E', 8],
    ['C', 'D', 2],
    ['C', 'G', 2],
    ['D', 'C', 2],
    ['D', 'F', 4],
    ['E', 'H', 10],
    ['F', 'E', 5],
    ['F', 'G', 5],
    ['G', 'H', 1]
]

graph = {}
for edge in edges:
    if edge[0] not in graph:
        graph[edge[0]] = []
    graph[edge[0]].append((edge[1], edge[2]))

# Ajouter tous les nœuds du graphe à g_scores
for node in nodes:
    if node not in graph:
        graph[node] = []

start_node = 'A'
goal_node = 'H'
came_from = {}

result = astar(graph, start_node, goal_node)
print(result)
