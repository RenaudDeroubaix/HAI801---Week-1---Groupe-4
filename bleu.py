from sacrebleu.metrics import BLEU
bleu_scorer = BLEU()

hypothesis = '''#include <iostream>
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
'''
reference = '''
#include <iostream>
#include <vector>
#include <queue>
#include <unordered_set>
#include <cmath> // pour std::abs

using namespace std;

// Structure représentant un nœud dans le graphe
struct Node {
    int g; // Coût réel depuis le départ
    int h; // Estimation du coût jusqu'à l'arrivée
    int index; // Indice du nœud dans le graphe

    // Constructeur
    Node(int g = 0, int h = 0, int index = -1) : g(g), h(h), index(index) {}

    // Fonction pour calculer le coût total f(n) = g(n) + h(n)
    int f() const {
        return g + h;
    }
};

// Structure représentant une arête
struct Edge {
    int a;
    int b;

    Edge(int a = 0, int b = 0) : a(a), b(b) {}
};

// Fonction pour estimer le coût restant (heuristique) à partir d'un nœud donné jusqu'à l'objectif
int heuristic(const Node& node, const Node& goal) {
    // Ici, vous pouvez implémenter votre propre heuristique, comme la distance de Manhattan ou la distance euclidienne
    return abs(node.index - goal.index);
}

// Fonction pour récupérer les voisins d'un nœud donné
vector<Node> getNeighbors(const Node& node, const vector<vector<int>>& graph) {
    vector<Node> neighbors;
    for (int neighbor_index : graph[node.index]) {
        neighbors.push_back(Node(0, 0, neighbor_index));
    }
    return neighbors;
}



// Fonction de comparaison pour la file de priorité
struct CompareNode {
    bool operator()(const Node& lhs, const Node& rhs) const {
        return lhs.f() > rhs.f();
    }
};

// Fonction A*
vector<Node> astar(const vector<vector<int>>& graph, const Node& start, const Node& goal) {
    priority_queue<Node, vector<Node>, CompareNode> open_list;
    unordered_set<int> closed_set;

    open_list.push(start);

    while (!open_list.empty()) {
        Node current_node = open_list.top();
        open_list.pop();

        if (current_node.index == goal.index) {
            // Chemin trouvé
            return {}; // Ici, vous devez implémenter la reconstruction du chemin et le retourner
        }

        closed_set.insert(current_node.index);

        // Récupérer les voisins du nœud courant
        vector<Node> neighbors = getNeighbors(current_node, graph);

        for (Node* neighbor_ptr : getNeighbors(current_node, graph)) {
    Node& neighbor = *neighbor_ptr;
    if (closed_set.find(neighbor.index) != closed_set.end()) {
        continue; // Ignorer les nœuds déjà visités
    }

    int tentative_g_score = current_node->g + 1; // Coût de l'arête (pour cet exemple, on suppose que tous les arêtes ont le même coût)

    if (tentative_g_score < neighbor.g) {
        neighbor.g = tentative_g_score;
        neighbor.h = heuristic(neighbor, goal);
        open_list.push(&neighbor); // Notez que vous devez pousser l'adresse du voisin dans la file de priorité
    }
}
    }

    return {}; // Aucun chemin trouvé
}

int main() {
    int nb_edges = 11;
    int nb_nodes = 8;

    // Définition du graphe
    vector<vector<int>> graph(nb_nodes);
    graph[0] = {1, 2, 3};
    graph[1] = {0, 4};
    graph[2] = {0, 5, 3};
    graph[3] = {0, 2, 6};
    graph[4] = {1, 7};
    graph[5] = {2, 7, 6};
    graph[6] = {3, 5, 7};
    graph[7] = {4, 5, 6};

    // Déclaration des nœuds de départ et d'arrivée
    Node start(0, 0, 0);
    Node goal(0, 0, 7);

    // Appel de la fonction A*
    vector<Node> path = astar(graph, start, goal);

    if (!path.empty()) {
        cout << "Chemin trouvé !" << endl;
        // Ici, vous pouvez imprimer le chemin trouvé
    } else {
        cout << "Aucun chemin trouvé." << endl;
    }

    return 0;
}
'''

score = bleu_scorer.sentence_score(
    hypothesis=hypothesis,
    references=[reference],
)

score.score

print(score)