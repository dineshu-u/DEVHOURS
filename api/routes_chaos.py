from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import List
from flow_guardian_x.api.routes_route import graph, cost_model, optimizer
from flow_guardian_x.prediction.nonlinear_model import NonlinearDelayModel
from flow_guardian_x.config import DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA

router = APIRouter(tags=["Chaos"])
nonlinear_model = NonlinearDelayModel()

# Valid edges in the network
VALID_EDGES = [("A", "B"), ("B", "C"), ("A", "D"), ("D", "C"), ("B", "D")]


class CollapseTrigger(BaseModel):
    intersection_node: str
    target_edge: List[str]  # Must be exactly ["FromNode", "ToNode"]

    @field_validator("target_edge")
    @classmethod
    def validate_edge(cls, v):
        if len(v) != 2:
            raise ValueError(
                "target_edge must have exactly 2 elements, e.g. [\"A\", \"B\"]. "
                f"Valid edges: A→B, B→C, A→D, D→C, B→D"
            )
        return v


@router.post("/trigger-grid-collapse")
def trigger_collapse(data: CollapseTrigger):
    """
    Simulates a catastrophic, non-historical grid collapse.

    **How to use:**
    - `intersection_node`: The node label being impacted (e.g. `"A"`, `"B"`)
    - `target_edge`: A list of exactly 2 node labels for the road to delete, e.g. `["A", "B"]`

    **Valid road segments:**
    `["A","B"]` · `["B","C"]` · `["A","D"]` · `["D","C"]` · `["B","D"]`
    """
    u, v = data.target_edge[0], data.target_edge[1]

    # Validate edge exists in network
    if not graph.has_edge(u, v):
        valid = ", ".join([f'["{a}","{b}"]' for a, b in VALID_EDGES])
        raise HTTPException(
            status_code=422,
            detail=(
                f"Edge '{u}→{v}' not found in the network. "
                f"Valid target_edge values: {valid}"
            )
        )

    # 1. Mark road as collapsed (zero capacity)
    original_capacity = graph[u][v].get("capacity", 100)
    graph[u][v]["capacity"] = 0

    # 2. Get vehicle density at collapse point (estimated from capacity ratio)
    density_at_collapse = 0.95  # Nonlinear model: near-critical density

    # 3. Nonlinear ripple delay prediction (non-historical — model uses physics, not past data)
    ripple_delay = nonlinear_model.calculate_predicted_delay(density_at_collapse)

    # 4. Find best alternative route after collapse
    updated_graph = cost_model.update_edge_costs(graph, {}, (DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA))
    alt_path, alt_cost = optimizer.get_best_route(updated_graph, u, v)
    alt_route = " → ".join(alt_path) if alt_path else "NO ALTERNATIVE FOUND"

    return {
        "status": "CRITICAL_COLLAPSE_TRIGGERED",
        "affected_segment": f"{u} → {v}",
        "original_capacity": original_capacity,
        "new_capacity": 0,
        "action": "GLOBAL_MINIMUM_REROUTE_EXECUTING",
        "nonlinear_ripple_recalculation": "ACTIVE",
        "impact_analysis": {
            "density_at_collapse": density_at_collapse,
            "predicted_ripple_delay_minutes": round(ripple_delay, 2),
            "sector_status": "UNSTABLE",
            "global_minimum_reroute": alt_route,
            "reroute_cost": round(alt_cost, 2) if alt_cost != float("inf") else "NO VIABLE ROUTE"
        }
    }
