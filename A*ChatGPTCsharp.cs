using System;
using System.Collections.Generic;

class AStar
{
    static Dictionary<char, int> nodes = new Dictionary<char, int> {
        { 'A', 9 }, { 'B', 3 }, { 'C', 5 }, { 'D', 6 },
        { 'E', 8 }, { 'F', 4 }, { 'G', 2 }, { 'H', 0 }
    };

    static List<Tuple<char, char, int>> edges = new List<Tuple<char, char, int>> {
        Tuple.Create('A', 'B', 2),
        Tuple.Create('A', 'C', 10),
        Tuple.Create('A', 'D', 3),
        Tuple.Create('B', 'E', 8),
        Tuple.Create('C', 'D', 2),
        Tuple.Create('C', 'G', 2),
        Tuple.Create('D', 'C', 2),
        Tuple.Create('D', 'F', 4),
        Tuple.Create('E', 'H', 10),
        Tuple.Create('F', 'E', 5),
        Tuple.Create('F', 'G', 5),
        Tuple.Create('G', 'H', 1)
    };

    static void Main()
    {
        Dictionary<char, List<Tuple<char, int>>> graph = new Dictionary<char, List<Tuple<char, int>>>();

        foreach (var edge in edges)
        {
            if (!graph.ContainsKey(edge.Item1))
            {
                graph[edge.Item1] = new List<Tuple<char, int>>();
            }
            graph[edge.Item1].Add(Tuple.Create(edge.Item2, edge.Item3));
        }

        char startNode = 'A';
        char goalNode = 'H';
        Dictionary<char, char> cameFrom = new Dictionary<char, char>();

        List<char> result = AStarSearch(graph, startNode, goalNode, cameFrom);
        Console.WriteLine(string.Join(" -> ", result));
    }

    static List<char> AStarSearch(Dictionary<char, List<Tuple<char, int>>> graph, char start, char goal, Dictionary<char, char> cameFrom)
    {
        PriorityQueue<Tuple<int, char>> openSet = new PriorityQueue<Tuple<int, char>>();
        openSet.Enqueue(Tuple.Create(0, start));

        Dictionary<char, int> gScores = new Dictionary<char, int>();
        foreach (var node in graph.Keys)
        {
            gScores[node] = int.MaxValue;
        }
        gScores[start] = 0;

        Dictionary<char, int> fScores = new Dictionary<char, int>();
        foreach (var node in graph.Keys)
        {
            fScores[node] = int.MaxValue;
        }
        fScores[start] = Heuristic(start, goal);

        while (openSet.Count > 0)
        {
            char current = openSet.Dequeue().Item2;

            if (current == goal)
            {
                return ReconstructPath(cameFrom, goal);
            }

            foreach (var neighbor in graph[current])
            {
                char nextNode = neighbor.Item1;
                int cost = neighbor.Item2;

                int tentativeGScore = gScores[current] + cost;

                if (tentativeGScore < gScores[nextNode])
                {
                    cameFrom[nextNode] = current;
                    gScores[nextNode] = tentativeGScore;
                    fScores[nextNode] = tentativeGScore + Heuristic(nextNode, goal);

                    if (!openSet.Contains(Tuple.Create(fScores[nextNode], nextNode)))
                    {
                        openSet.Enqueue(Tuple.Create(fScores[nextNode], nextNode));
                    }
                }
            }
        }

        return new List<char>();
    }

    static int Heuristic(char node, char goal)
    {
        return nodes[goal];
    }

    static List<char> ReconstructPath(Dictionary<char, char> cameFrom, char current)
    {
        List<char> path = new List<char>();
        while (cameFrom.ContainsKey(current))
        {
            path.Add(current);
            current = cameFrom[current];
        }
        path.Reverse();
        return path;
    }

    // Priority Queue implementation
    public class PriorityQueue<T> where T : IComparable<T>
    {
        private List<T> elements = new List<T>();

        public int Count
        {
            get { return elements.Count; }
        }

        public void Enqueue(T item)
        {
            elements.Add(item);
            int ci = elements.Count - 1;
            while (ci > 0)
            {
                int pi = (ci - 1) / 2;
                if (elements[ci].CompareTo(elements[pi]) >= 0)
                    break;
                T tmp = elements[ci];
                elements[ci] = elements[pi];
                elements[pi] = tmp;
                ci = pi;
            }
        }

        public T Dequeue()
        {
            int li = elements.Count - 1;
            T frontItem = elements[0];
            elements[0] = elements[li];
            elements.RemoveAt(li);

            --li;
            int pi = 0;
            while (true)
            {
                int ci = pi * 2 + 1;
                if (ci > li)
                    break;
                int rc = ci + 1;
                if (rc <= li && elements[rc].CompareTo(elements[ci]) < 0)
                    ci = rc;
                if (elements[pi].CompareTo(elements[ci]) <= 0)
                    break;
                T tmp = elements[pi];
                elements[pi] = elements[ci];
                elements[ci] = tmp;
                pi = ci;
            }
            return frontItem;
        }

        public bool Contains(T item)
        {
            return elements.Contains(item);
        }
    }
}
