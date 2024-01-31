import heapq

class Node:
    def __init__(self, name, h, aretes=None):
        self.name = name
        self.h = h
        self.aretes = aretes if aretes is not None else []

    def getF(self, cost):
        return cost + self.h

    def add_voisins(self, a):
        self.aretes.append(a)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Edge:
    def __init__(self, A, B, g):
        self.A = A
        self.B = B
        self.g = g

class CompareF:
    def __init__(self, f_score):
        self.f_score = f_score

    def __lt__(self, a, b):
        if self.f_score[a] == self.f_score[b]:
            return id(a) < id(b)
        return self.f_score[a] < self.f_score[b]

def a_star(depart, but):
    g_score = {depart: 0}
    f_score = {depart: depart.getF(0)}
    came_from = {}
    counter = 0  # Unique identifier

    open_set = [(f_score[depart], counter, depart)]
    heapq.heapify(open_set)

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current == but:
            # Reconstruit le chemin
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for edge in current.aretes:
            neighbor = edge.B if edge.A == current else edge.A
            tentative_g_score = g_score[current] + edge.g

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = neighbor.getF(tentative_g_score)
                counter += 1
                heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))

    # If the loop completes and no path is found, return an empty list
    return []

if __name__ == "__main__":
    A = Node("A", 9)
    B = Node("B", 3)
    C = Node("C", 5)
    D = Node("D", 6)
    E = Node("E", 8)
    F = Node("F", 4)
    G = Node("G", 2)
    H = Node("H", 0)

    ab = Edge(A, B, 8)
    be = Edge(B, E, 8)
    eh = Edge(E, H, 10)
    ac = Edge(A, C, 10)
    ad = Edge(A, D, 3)
    cd = Edge(C, D, 2)
    cg = Edge(C, G, 2)
    df = Edge(D, F, 4)
    fg = Edge(F, G, 5)
    gh = Edge(G, H, 1)
    ef = Edge(E, F, 5)

    A.add_voisins(ab)
    A.add_voisins(ac)
    A.add_voisins(ad)
    B.add_voisins(ab)
    B.add_voisins(be)
    C.add_voisins(ac)
    C.add_voisins(cd)
    C.add_voisins(cg)
    D.add_voisins(ad)
    D.add_voisins(cd)
    D.add_voisins(df)
    E.add_voisins(be)
    E.add_voisins(eh)
    E.add_voisins(ef)
    F.add_voisins(df)
    F.add_voisins(fg)
    F.add_voisins(ef)
    G.add_voisins(fg)
    G.add_voisins(gh)
    H.add_voisins(eh)
    H.add_voisins(gh)

    res = a_star(A, H)
    print([node.name for node in res])
