class RerouteManager:
    def __init__(self, optimizer):
        self.optimizer = optimizer

    def manage_rerouting(self, graph, start, end):
        """Computes and formats the reroute recommendation."""
        path, cost = self.optimizer.get_best_route(graph, start, end)
        if path:
            return {
                "status": "SUCCESS",
                "recommended_route": " -> ".join(path),
                "total_cost": cost
            }
        return {"status": "FAILED", "message": "No path found"}
