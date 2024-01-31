import java.util.*;

class AStar {
    static HashMap<Character, Integer> nodes = new HashMap<Character, Integer>() {{
        put('A', 9);
        put('B', 3);
        put('C', 5);
        put('D', 6);
        put('E', 8);
        put('F', 4);
        put('G', 2);
        put('H', 0);
    }};

    static List<List<Object>> edges = Arrays.asList(
        Arrays.asList('A', 'B', 2),
        Arrays.asList('A', 'C', 10),
        Arrays.asList('A', 'D', 3),
        Arrays.asList('B', 'E', 8),
        Arrays.asList('C', 'D', 2),
        Arrays.asList('C', 'G', 2),
        Arrays.asList('D', 'C', 2),
        Arrays.asList('D', 'F', 4),
        Arrays.asList('E', 'H', 10),
        Arrays.asList('F', 'E', 5),
        Arrays.asList('F', 'G', 5),
        Arrays.asList('G', 'H', 1)
    );

    public static void main(String[] args) {
        HashMap<Character, List<Pair<Character, Integer>>> graph = new HashMap<>();
        for (List<Object> edge : edges) {
            char node = (char) edge.get(0);
            char neighbor = (char) edge.get(1);
            int cost = (int) edge.get(2);

            graph.putIfAbsent(node, new ArrayList<>());
            graph.get(node).add(new Pair<>(neighbor, cost));
        }

        char startNode = 'A';
        char goalNode = 'H';
        HashMap<Character, Character> cameFrom = new HashMap<>();

        List<Character> result = aStarSearch(graph, startNode, goalNode, cameFrom);
        System.out.println(result);
    }

    static List<Character> aStarSearch(HashMap<Character, List<Pair<Character, Integer>>> graph, char start, char goal, HashMap<Character, Character> cameFrom) {
        PriorityQueue<Pair<Integer, Character>> openSet = new PriorityQueue<>(Comparator.comparingInt(Pair::getKey));
        openSet.add(new Pair<>(0, start));

        HashMap<Character, Integer> gScores = new HashMap<>();
        for (char node : graph.keySet()) {
            gScores.put(node, Integer.MAX_VALUE);
        }
        gScores.put(start, 0);

        HashMap<Character, Integer> fScores = new HashMap<>();
        for (char node : graph.keySet()) {
            fScores.put(node, Integer.MAX_VALUE);
        }
        fScores.put(start, heuristic(start, goal));

        while (!openSet.isEmpty()) {
            char current = openSet.poll().getValue();

            if (current == goal) {
                return reconstructPath(cameFrom, goal);
            }

            for (Pair<Character, Integer> neighbor : graph.get(current)) {
                char nextNode = neighbor.getKey();
                int cost = neighbor.getValue();

                int tentativeGScore = gScores.get(current) + cost;

                if (tentativeGScore < gScores.get(nextNode)) {
                    cameFrom.put(nextNode, current);
                    gScores.put(nextNode, tentativeGScore);
                    fScores.put(nextNode, tentativeGScore + heuristic(nextNode, goal));

                    openSet.add(new Pair<>(fScores.get(nextNode), nextNode));
                }
            }
        }

        return new ArrayList<>();
    }

    static int heuristic(char node, char goal) {
        return nodes.get(goal);
    }

    static List<Character> reconstructPath(HashMap<Character, Character> cameFrom, char current) {
        List<Character> path = new ArrayList<>();
        while (cameFrom.containsKey(current)) {
            path.add(current);
            current = cameFrom.get(current);
        }
        path.add(current);
        Collections.reverse(path);
        return path;
    }

    static class Pair<K, V> {
        private K key;
        private V value;

        public Pair(K key, V value) {
            this.key = key;
            this.value = value;
        }

        public K getKey() {
            return key;
        }

        public V getValue() {
            return value;
        }
    }
}
