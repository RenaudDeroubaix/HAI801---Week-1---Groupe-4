class Node {
    constructor(name, heuristic) {
        this.name = name;
        this.heuristic = heuristic;
        this.g = Infinity;  // Distance from start node
        this.f = Infinity;  // Total estimated cost of the cheapest solution through this node
        this.adjacent = {};  // Adjacent nodes and their costs
        this.parent = null;  // Parent node in the path
    }

    addEdge(neighbor, cost) {
        this.adjacent[neighbor] = cost;
    }
}

function astar(graph, start, end) {
    const startNode = graph[start];
    startNode.g = 0;
    startNode.f = startNode.heuristic;

    const openList = [startNode];
    const closedSet = new Set();

    while (openList.length > 0) {
        let currentNode = openList.shift();
        closedSet.add(currentNode);

        if (currentNode.name === end) {
            const path = [];
            while (currentNode) {
                path.push(currentNode.name);
                currentNode = currentNode.parent;
            }
            return path.reverse();  // Return reversed path
        }

        for (const [adj, cost] of Object.entries(currentNode.adjacent)) {
            const childNode = graph[adj];
            if (closedSet.has(childNode)) {
                continue;
            }

            const tentativeGScore = currentNode.g + cost;

            if (tentativeGScore < childNode.g) {
                childNode.parent = currentNode;
                childNode.g = tentativeGScore;
                childNode.f = tentativeGScore + childNode.heuristic;

                if (!openList.includes(childNode)) {
                    openList.push(childNode);
                }
            }
        }
    }

    return null;
}

const nodes = {};
const heuristics = { 'A': 9, 'B': 3, 'C': 5, 'D': 6, 'E': 8, 'F': 4, 'G': 2, 'H': 0 };
for (const [node, hVal] of Object.entries(heuristics)) {
    nodes[node] = new Node(node, hVal);
}

const edges = [
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
];

for (const edge of edges) {
    nodes[edge[0]].addEdge(edge[1], edge[2]);
}

const path = astar(nodes, 'A', 'H');
console.log("Path found by A*:", path);
