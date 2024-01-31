class PriorityQueue {
    constructor() {
        this.elements = [];
    }

    enqueue(element) {
        this.elements.push(element);
        this.sort();
    }

    dequeue() {
        return this.elements.shift();
    }

    sort() {
        this.elements.sort((a, b) => a[0] - b[0]);
    }

    isEmpty() {
        return this.elements.length === 0;
    }
}

const nodes = { 'A': 9, 'B': 3, 'C': 5, 'D': 6, 'E': 8, 'F': 4, 'G': 2, 'H': 0 };
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

function astar(graph, start, goal) {
    const openSet = new PriorityQueue();
    openSet.enqueue([0, start]);

    const cameFrom = {};
    const gScores = {};
    const fScores = {};

    Object.keys(graph).forEach(node => {
        gScores[node] = Infinity;
        fScores[node] = Infinity;
    });

    gScores[start] = 0;
    fScores[start] = heuristic(start, goal);

    while (!openSet.isEmpty()) {
        const current = openSet.dequeue()[1];

        if (current === goal) {
            return reconstructPath(cameFrom, goal);
        }

        for (const [neighbor, cost] of graph[current]) {
            const tentativeGScore = gScores[current] + cost;

            if (tentativeGScore < gScores[neighbor]) {
                cameFrom[neighbor] = current;
                gScores[neighbor] = tentativeGScore;
                fScores[neighbor] = tentativeGScore + heuristic(neighbor, goal);

                if (!openSet.elements.some(el => el[1] === neighbor)) {
                    openSet.enqueue([fScores[neighbor], neighbor]);
                }
            }
        }
    }

    return [];
}

function heuristic(node, goal) {
    return nodes[goal];
}

function reconstructPath(cameFrom, current) {
    const path = [current];
    while (cameFrom[current] !== undefined) {
        current = cameFrom[current];
        path.push(current);
    }
    return path.reverse();
}

const graph = {};
for (const edge of edges) {
    const [start, end, cost] = edge;
    if (!graph[start]) {
        graph[start] = [];
    }
    graph[start].push([end, cost]);
}

const startNode = 'A';
const goalNode = 'H';

const result = astar(graph, startNode, goalNode);
console.log(result);
