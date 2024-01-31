#include <iostream>
#include <vector>
#include <queue>
#include <cmath>
#include <algorithm>
#include <unordered_map>

using namespace std;


struct Edge;

struct Node {
    string name;  // Node identifier
    int h;        // coût heuristique vers l'objectif
    vector<Edge> aretes;  // liste des voisins

    Node(string name, int h, vector<Edge> aretes) : name(name), h(h), aretes(aretes) {}
    Node(string name, int h) : name(name), h(h) {}

    // Fonction pour calculer le coût total (f = g + h)
    int getF(int cost) const {
        return cost + h;
    }

    void addVoisins(Edge a);

    // Define the == operator for Node
    bool operator==(const Node& other) const {
        return name == other.name;
    }
};

struct Edge {
    Node* A;  // arrete entre A et B
    Node* B;
    int g;    // cost
    Edge(Node* A, Node* B, int g) : A(A), B(B), g(g) {}
};

// Define addVoisins here
void Node::addVoisins(Edge a) {
    aretes.push_back(a);
}

// Custom comparator for priority queue based on f = g + h
struct CompareF {
    bool operator()(const pair<int, Node*>& a, const pair<int, Node*>& b) {
        return a.first > b.first;
    }
};

vector<Node> aStar(Node& depart, Node& but) {
    unordered_map<Node*, int> gScore;  // cout de depart jusuq'a la node
    unordered_map<Node*, int> fScore;  // Estimated total cost from start to goal passing through node Cout total estimé du depart jusuq'au but passant par la node
    unordered_map<Node*, Node*> cameFrom;  // chemin du parent

    priority_queue<pair<int, Node*>, vector<pair<int, Node*>>, CompareF> openSet;

    gScore[&depart] = 0;
    fScore[&depart] = depart.getF(0);
    openSet.push({fScore[&depart], &depart});

    while (!openSet.empty()) {
        Node* current = openSet.top().second;
        openSet.pop();

        if (*current == but) {
            // Reconstruit le chemin
            vector<Node> path;
            while (current != &depart) {
                path.push_back(*current);
                current = cameFrom[current];
            }
            path.push_back(depart);
            reverse(path.begin(), path.end());
            return path;
        }

        for (const Edge& edge : current->aretes) {
            Node* neighbor = (edge.A == current) ? edge.B : edge.A;
            int tentativeGScore = gScore[current] + edge.g;

            if (gScore.find(neighbor) == gScore.end() || tentativeGScore < gScore[neighbor]) {
                cameFrom[neighbor] = current;
                gScore[neighbor] = tentativeGScore;
                fScore[neighbor] = neighbor->getF(tentativeGScore);
                openSet.push({fScore[neighbor], neighbor});
            }
        }
    }

    // pas de chemin
    return vector<Node>();
}

int main() {
    Node A("A", 9), B("B", 3), C("C", 5), D("D", 6), E("E", 8), F("F", 4), G("G", 2), H("H", 0);
    Edge ab(&A, &B, 8), be(&B, &E, 8), eh(&E, &H, 10), ac(&A, &C, 10), ad(&A, &D, 3), cd(&C, &D, 2), cg(&C, &G, 2),
        df(&D, &F, 4), fg(&F, &G, 5), gh(&G, &H, 1), ef(&E, &F, 5);
    A.addVoisins(ab);
    A.addVoisins(ac);
    A.addVoisins(ad);
    B.addVoisins(ab);
    B.addVoisins(be);
    C.addVoisins(ac);
    C.addVoisins(cd);
    C.addVoisins(cg);
    D.addVoisins(ad);
    D.addVoisins(cd);
    D.addVoisins(df);
    E.addVoisins(be);
    E.addVoisins(eh);
    E.addVoisins(ef);
    F.addVoisins(df);
    F.addVoisins(fg);
    F.addVoisins(ef);
    G.addVoisins(fg);
    G.addVoisins(gh);
    H.addVoisins(eh);
    H.addVoisins(gh);

    vector<Node> res = aStar(A, H);
    for (int i = 0; i < res.size(); i++) {
        cout << res[i].name << " ";
    }
    cout << endl;
}
