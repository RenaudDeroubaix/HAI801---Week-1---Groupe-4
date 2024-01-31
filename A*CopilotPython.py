import heapq

def a_star(graph, start, end):
    queue = []
    heapq.heappush(queue, (0, start))
    costs = {node: float('inf') for node in graph}
    costs[start] = 0
    parents = {start: None}

    while queue:
        current_cost, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
                parents[neighbor] = current_node

    return parents, costs

graph = {
    'A': {'B': 2, 'C': 10, 'D': 3},
    'B': {'E': 8},
    'C': {'D': 2, 'G': 2},
    'D': {'C': 2, 'F': 4},
    'E': {'H': 10},
    'F': {'E': 5, 'G': 5},
    'G': {'H': 1},
    'H': {}
}

def reconstruct_path(parents, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parents[path[-1]])
    path.reverse()
    return path

parents, costs = a_star(graph, 'A', 'H')
path = reconstruct_path(parents, 'A', 'H')
print('Path:', path)