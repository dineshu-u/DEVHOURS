import networkx as nx

class GraphBuilder:
    @staticmethod
    def build_default_graph():
        """Creates a sample road network graph."""
        G = nx.DiGraph()
        
        # Nodes: Intersections
        # Edges: Roads with initial capacities
        edges = [
            ("A", "B", {"capacity": 100, "length": 5}),
            ("B", "C", {"capacity": 80, "length": 3}),
            ("A", "D", {"capacity": 120, "length": 6}),
            ("D", "C", {"capacity": 100, "length": 4}),
            ("B", "D", {"capacity": 50, "length": 2})
        ]
        G.add_edges_from([(u, v, d) for u, v, d in edges])
        return G
