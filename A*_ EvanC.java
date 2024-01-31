import java.util.*;

public class Node {
    public String id;
    public Node parent = null;

    public List<Edge> neighbors;

    public int FCost = Integer.MAX_VALUE;
    public int gCost = Integer.MAX_VALUE;
    public int hCost; 

    Node(int h,String id){
          this.hCost = h;
          this.id = id;
          this.neighbors = new ArrayList<>();
    }

    public static class Edge {
          Edge(int cost, Node node){
                this.cost = cost;
                this.node = node;
          }

          public int cost;
          public Node node;
    }

    public void addBranch(int weight, Node node){
          Edge newEdge = new Edge(weight, node);
          neighbors.add(newEdge);
    }

    public int calculateHeuristic(Node target){
          return this.hCost;
    }
}


import java.util.*;


public class PathFinding {
	
    public static Node aStar(Node startNode, Node goalNode){
	    List<Node> frontier = new ArrayList<>();
	    HashSet<Node> explored = new HashSet<>();
	    
	    startNode.FCost = startNode.gCost + startNode.calculateHeuristic(goalNode);
	    frontier.add(startNode);

	    while(!frontier.isEmpty()){
	    	
	        Node currentNode = frontier.get(0);
	        
	        for (Node eachNode : frontier) {
				if(eachNode.FCost<currentNode.FCost)
					currentNode=eachNode;
			}
	        
	        if(currentNode == goalNode){
	            return currentNode;
	        }

	        for(Node.Edge edge : currentNode.neighbors){
	            Node neighbour = edge.node;
	            
	            int totalWeight = currentNode.gCost + edge.cost;

	            if(!frontier.contains(neighbour) && !explored.contains(neighbour)){
	            	neighbour.parent = currentNode;
	            	neighbour.gCost = totalWeight;
	            	neighbour.FCost = neighbour.gCost + neighbour.calculateHeuristic(goalNode);
	                frontier.add(neighbour);
	            } else {
	                if(totalWeight < neighbour.gCost){
	                	neighbour.parent = currentNode;
	                	neighbour.gCost = totalWeight;
	                	neighbour.FCost = neighbour.gCost + neighbour.calculateHeuristic(goalNode);

	                    if(explored.contains(neighbour)){
	                        explored.remove(neighbour);
	                        frontier.add(neighbour);
	                    }
	                }
	            }
	        }

	        frontier.remove(currentNode);
	        explored.add(currentNode);
	    }
	    return null;
	}
    
    public static int pathCost(Node startNode,Node goalNode) {
    	List<String> idas=new ArrayList<>();
    	Node target=goalNode;
    	idas.add(goalNode.id);
    	while(target!=startNode) {
    		target=target.parent;
    		idas.add(target.id);
    	}
    	
    	int x=goalNode.hCost;
    	
    	for (int i = idas.size()-1; i > 0; i--) {
    		for (Node.Edge edge : startNode.neighbors) {
    			if(edge.node.id.equals(idas.get(i-1))){
    				x+=edge.cost;
    				startNode=edge.node;
    			}
    			
			}
		}
    	return x;
    }

	public static void printPath(Node goalNode){
	    Node currentNode = goalNode;

	    if(currentNode==null)
	        return;

	    List<String> ids = new ArrayList<>();

	    while(currentNode.parent != null){
	        ids.add(currentNode.id);
	        currentNode = currentNode.parent;
	    }
	    ids.add(currentNode.id);
	    Collections.reverse(ids);
	    String s="";
	    for(String id : ids){
	    	s+=id + " -> ";
	    }
	    System.out.println("Path\t  : "+s.substring(0, s.length()-3));
	}
}

import java.util.*;

public class Node {
	public String id;
	public Node parent = null;

	public List<Edge> neighbors;

	public int FCost = Integer.MAX_VALUE;
	public int gCost = Integer.MAX_VALUE;
	public int hCost;

	Node(int h,String id){
		this.hCost = h;
		this.id = id;
		this.neighbors = new ArrayList<>();
	}

	public static class Edge {
		Edge(int cost, Node node){
			this.cost = cost;
			this.node = node;
		}

		public int cost;
		public Node node;
	}

	public void addBranch(int weight, Node node){
		Edge newEdge = new Edge(weight, node);
		neighbors.add(newEdge);
	}

	public int calculateHeuristic(Node target){
		return this.hCost;
	}
}

import java.util.*;


public class PathFinding {

	public static Node aStar(Node startNode, Node goalNode){
		List<Node> frontier = new ArrayList<>();
		HashSet<Node> explored = new HashSet<>();

		startNode.FCost = startNode.gCost + startNode.calculateHeuristic(goalNode);
		frontier.add(startNode);

		while(!frontier.isEmpty()){

			Node currentNode = frontier.get(0);

			for (Node eachNode : frontier) {
				if(eachNode.FCost<currentNode.FCost)
					currentNode=eachNode;
			}

			if(currentNode == goalNode){
				return currentNode;
			}

			for(Node.Edge edge : currentNode.neighbors){
				Node neighbour = edge.node;

				int totalWeight = currentNode.gCost + edge.cost;

				if(!frontier.contains(neighbour) && !explored.contains(neighbour)){
					neighbour.parent = currentNode;
					neighbour.gCost = totalWeight;
					neighbour.FCost = neighbour.gCost + neighbour.calculateHeuristic(goalNode);
					frontier.add(neighbour);
				} else {
					if(totalWeight < neighbour.gCost){
						neighbour.parent = currentNode;
						neighbour.gCost = totalWeight;
						neighbour.FCost = neighbour.gCost + neighbour.calculateHeuristic(goalNode);

						if(explored.contains(neighbour)){
							explored.remove(neighbour);
							frontier.add(neighbour);
						}
					}
				}
			}

			frontier.remove(currentNode);
			explored.add(currentNode);
		}
		return null;
	}

	public static int pathCost(Node startNode,Node goalNode) {
		List<String> idas=new ArrayList<>();
		Node target=goalNode;
		idas.add(goalNode.id);
		while(target!=startNode) {
			target=target.parent;
			idas.add(target.id);
		}

		int x=goalNode.hCost;

		for (int i = idas.size()-1; i > 0; i--) {
			for (Node.Edge edge : startNode.neighbors) {
				if(edge.node.id.equals(idas.get(i-1))){
					x+=edge.cost;
					startNode=edge.node;
				}

			}
		}
		return x;
	}

	public static void printPath(Node goalNode){
		Node currentNode = goalNode;

		if(currentNode==null)
			return;

		List<String> ids = new ArrayList<>();

		while(currentNode.parent != null){
			ids.add(currentNode.id);
			currentNode = currentNode.parent;
		}
		ids.add(currentNode.id);
		Collections.reverse(ids);
		String s="";
		for(String id : ids){
			s+=id + " -> ";
		}
		System.out.println("Path\t  : "+s.substring(0, s.length()-3));
	}
}


public class test {
	public static void main(String[] args) {

		Node a = new Node(9, "A");
		Node b = new Node(3, "B");
		Node c = new Node(5, "C");
		Node d = new Node(6, "D");
		Node e = new Node(8, "F");
		Node f = new Node(4, "G");
		Node g = new Node(2, "G");
		Node h = new Node(0, "H");


		a.addBranch(2, b);
		a.addBranch(3, d);
		a.addBranch(10, c);

		b.addBranch(2, a);

		c.addBranch(10, a);
		c.addBranch(2, d);
		c.addBranch(2, g);

		d.addBranch(3, b);
		d.addBranch(2, b);
		d.addBranch(4, b);

		e.addBranch(8, a);
		e.addBranch(5, c);
		e.addBranch(10, f);

		f.addBranch(5, e);
		f.addBranch(4, d);
		f.addBranch(5, g);

		g.addBranch(2, f);
		g.addBranch(5, h);
		g.addBranch(9, c);

		h.addBranch(1, g);
		h.addBranch(10, e);

		Node path = PathFinding.aStar(a, g);
		PathFinding.printPath(path);
		int pathCost = PathFinding.pathCost(a, h);
		System.out.println("Path Cost : " + pathCost);
	}
}