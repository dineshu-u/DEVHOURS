from fastapi import APIRouter
from flow_guardian_x.routing.graph_builder import GraphBuilder
from flow_guardian_x.routing.cost_model import CostModel
from flow_guardian_x.routing.route_optimizer import RouteOptimizer
from flow_guardian_x.config import DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA, EMERGENCY_ALPHA, EMERGENCY_BETA, EMERGENCY_GAMMA

router = APIRouter(tags=["Routing"])

# Initialize routing components
graph = GraphBuilder.build_default_graph()
cost_model = CostModel()
optimizer = RouteOptimizer()

@router.get("/route")
def get_optimal_route(start: str, end: str, is_emergency: bool = False):
    # 1. Select Weights
    alpha = EMERGENCY_ALPHA if is_emergency else DEFAULT_ALPHA
    beta = EMERGENCY_BETA if is_emergency else DEFAULT_BETA
    gamma = EMERGENCY_GAMMA if is_emergency else DEFAULT_GAMMA
    
    # 2. Update Costs — pass weights as tuple (alpha, beta, gamma)
    updated_graph = cost_model.update_edge_costs(graph, {}, (alpha, beta, gamma))
    
    # 3. Find Best Route
    path, cost = optimizer.get_best_route(updated_graph, start, end)
    
    if not path:
        return {"status": "FAILED", "message": "No path found between nodes."}
        
    return {
        "status": "SUCCESS",
        "recommended_route": " -> ".join(path),
        "total_optimization_cost": round(cost, 2),
        "priority_mode": "EMERGENCY" if is_emergency else "NORMAL"
    }
