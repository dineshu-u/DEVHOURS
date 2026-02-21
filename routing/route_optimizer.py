import networkx as nx

class RouteOptimizer:
    @staticmethod
    def get_best_route(graph, start_node, end_node):
        """Runs Dijkstra algorithm to compute best route based on 'weight'."""
        try:
            path = nx.dijkstra_path(graph, source=start_node, target=end_node, weight="weight")
            cost = nx.dijkstra_path_length(graph, source=start_node, target=end_node, weight="weight")
            return path, cost
        except nx.NetworkXNoPath:
            return None, float('inf')
