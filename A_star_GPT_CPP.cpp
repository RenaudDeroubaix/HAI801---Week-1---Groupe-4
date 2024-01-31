#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <limits>
#include <algorithm>
std::unordered_map<char, int> nodes = {
    {'A', 9}, {'B', 3}, {'C', 5}, {'D', 6},
    {'E', 8}, {'F', 4}, {'G', 2}, {'H', 0}
};

std::vector<std::tuple<char, char, int>> edges = {
    std::make_tuple('A', 'B', 2),
    std::make_tuple('A', 'C', 10),
    std::make_tuple('A', 'D', 3),
    std::make_tuple('B', 'E', 8),
    std::make_tuple('C', 'D', 2),
    std::make_tuple('C', 'G', 2),
    std::make_tuple('D', 'C', 2),
    std::make_tuple('D', 'F', 4),
    std::make_tuple('E', 'H', 10),
    std::make_tuple('F', 'E', 5),
    std::make_tuple('F', 'G', 5),
    std::make_tuple('G', 'H', 1)
};

std::vector<char> AStarSearch(const std::unordered_map<char, std::vector<std::tuple<char, int>>>& graph,
                              char start, char goal, std::unordered_map<char, char>& cameFrom);

int Heuristic(char node, char goal);

std::vector<char> ReconstructPath(const std::unordered_map<char, char>& cameFrom, char current);

int main() {
    std::unordered_map<char, std::vector<std::tuple<char, int>>> graph;

    for (const auto& edge : edges) {
        if (graph.find(std::get<0>(edge)) == graph.end()) {
            graph[std::get<0>(edge)] = {};
        }
        graph[std::get<0>(edge)].emplace_back(std::get<1>(edge), std::get<2>(edge));
    }

    char startNode = 'A';
    char goalNode = 'H';
    std::unordered_map<char, char> cameFrom;

    std::vector<char> result = AStarSearch(graph, startNode, goalNode, cameFrom);

    for (char node : result) {
        std::cout << node << " -> ";
    }

    return 0;
}

std::vector<char> AStarSearch(const std::unordered_map<char, std::vector<std::tuple<char, int>>>& graph,
                              char start, char goal, std::unordered_map<char, char>& cameFrom) {
    std::priority_queue<std::tuple<int, char>, std::vector<std::tuple<int, char>>, std::greater<std::tuple<int, char>>> openSet;
    openSet.push(std::make_tuple(0, start));

    std::unordered_map<char, int> gScores;
    for (const auto& node : graph) {
        gScores[node.first] = std::numeric_limits<int>::max();
    }
    gScores[start] = 0;

    std::unordered_map<char, int> fScores;
    for (const auto& node : graph) {
        fScores[node.first] = std::numeric_limits<int>::max();
    }
    fScores[start] = Heuristic(start, goal);

    while (!openSet.empty()) {
        char current = std::get<1>(openSet.top());
        openSet.pop();

        if (current == goal) {
            return ReconstructPath(cameFrom, goal);
        }

        for (const auto& neighbor : graph.at(current)) {
            char nextNode = std::get<0>(neighbor);
            int cost = std::get<1>(neighbor);

            int tentativeGScore = gScores[current] + cost;

            if (tentativeGScore < gScores[nextNode]) {
                cameFrom[nextNode] = current;
                gScores[nextNode] = tentativeGScore;
                fScores[nextNode] = tentativeGScore + Heuristic(nextNode, goal);

                openSet.push(std::make_tuple(fScores[nextNode], nextNode));
            }
        }
    }

    return {};
}

int Heuristic(char node, char goal) {
    return nodes[goal];
}

std::vector<char> ReconstructPath(const std::unordered_map<char, char>& cameFrom, char current) {
    std::vector<char> path;
    while (cameFrom.find(current) != cameFrom.end()) {
        path.push_back(current);
        current = cameFrom.at(current);
    }
    path.push_back(current);
    std::reverse(path.begin(), path.end());
    return path;
}
