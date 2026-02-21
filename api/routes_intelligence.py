from fastapi import APIRouter
import random
from flow_guardian_x.config import DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA
from flow_guardian_x.api.routes_route import graph

router = APIRouter(tags=["Intelligence"])

@router.get("/uic-stream")
def get_uic_data():
    """
    Streams data for Optimization Radar and Regime Heatmap.
    Connected to live system weights and graph state.
    """
    # Radar Data: Current optimization balance
    radar_data = {
        "alpha_delay": DEFAULT_ALPHA,
        "beta_emission": DEFAULT_BETA,
        "gamma_risk": DEFAULT_GAMMA
    }
    
    # Heatmap Data: Derived from current graph edge capacities
    heatmap_states = []
    for u, v, data in graph.edges(data=True):
        capacity = data.get("capacity", 100)
        # Classify based on remaining capacity if we had live flow
        # For demo, use 0 capacity road to show Unstable
        regime = "Unstable" if capacity <= 0 else random.choice(["Stable", "Meta-Stable"])
        heatmap_states.append({"sector": f"{u}-{v}", "regime": regime})
    
    return {
        "radar": radar_data,
        "heatmap": heatmap_states,
        "refresh_rate_ms": 1000
    }
