function aStar(nodes, edges, start, end) {
    let costs = {};
    let parents = {};
    let queue = [];

    for (let node in nodes) {
        costs[node] = Infinity;
    }
    costs[start] = 0;

    queue.push(start);

    while (queue.length > 0) {
        let current = queue.shift();

        for (let i = 0; i < edges.length; i++) {
            let [node1, node2, cost] = edges[i];

            if (node1 === current && costs[node2] > costs[node1] + cost) {
                costs[node2] = costs[node1] + cost;
                parents[node2] = node1;

                if (!queue.includes(node2)) {
                    queue.push(node2);
                }
            }
        }
    }

    return {costs, parents};
}

let nodes = { 'A': 9, 'B': 3, 'C': 5, 'D': 6, 'E': 8, 'F': 4, 'G': 2, 'H': 0 };
let edges = [
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

function reconstructPath(parents, start, end) {
    let path = [end];
    while (path[path.length - 1] !== start) {
        path.push(parents[path[path.length - 1]]);
    }
    return path.reverse();
}

let result = aStar(nodes, edges, 'A', 'H');
let path = reconstructPath(result.parents, 'A', 'H');
console.log('Path:', path);