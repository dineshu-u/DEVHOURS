from flow_guardian_x.decision_engine.objective_function import ObjectiveFunction

class CostModel:
    def __init__(self):
        self.obj_fn = ObjectiveFunction()

    def update_edge_costs(self, graph, traffic_data, weights):
        """
        Assigns weight to each road using objective function output.
        traffic_data: dict mapping (u, v) to traffic metrics.
        weights: (alpha, beta, gamma)
        """
        alpha, beta, gamma = weights
        for u, v, data in graph.edges(data=True):
            edge_metrics = traffic_data.get((u, v), {
                "predicted_delay": 0,
                "emission_load": 0,
                "bottleneck_risk": 0
            })
            
            # Check for grid collapse (Zero Capacity)
            capacity = data.get("capacity", 1)
            if capacity <= 0:
                cost = float('inf') # Impassable
            else:
                cost = self.obj_fn.calculate_cost(
                    edge_metrics["predicted_delay"],
                    edge_metrics["emission_load"],
                    edge_metrics["bottleneck_risk"],
                    alpha, beta, gamma
                )
            
            # Incorporate physical length into cost as well
            base_length = data.get("length", 1)
            graph[u][v]["weight"] = base_length + cost if cost != float('inf') else float('inf')
        return graph
