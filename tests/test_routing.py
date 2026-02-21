from flow_guardian_x.routing.graph_builder import GraphBuilder
from flow_guardian_x.routing.route_optimizer import RouteOptimizer
from flow_guardian_x.routing.cost_model import CostModel

def test_routing_logic():
    graph = GraphBuilder.build_default_graph()
    optimizer = RouteOptimizer()
    cost_model = CostModel()
    
    # Update costs with uniform metrics
    weights = (0.6, 0.2, 0.2)
    traffic_data = {} # all zeros
    graph = cost_model.update_edge_costs(graph, traffic_data, weights)
    
    path, cost = optimizer.get_best_route(graph, "A", "C")
    
    assert path is not None
    assert "A" in path
    assert "C" in path
    assert cost > 0
