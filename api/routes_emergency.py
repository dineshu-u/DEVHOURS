from fastapi import APIRouter
from flow_guardian_x.emergency_control.priority_logic import PriorityLogic

router = APIRouter(tags=["Emergency"])
emergency_logic = PriorityLogic()

@router.post("/emergency")
def trigger_emergency_mode(intersection_id: str):
    """
    Activates prioritized emergency routing and physical signal control.
    """
    weights = emergency_logic.get_priority_weights()
    return {
        "status": "EMERGENCY_ACTIVE",
        "intersection": intersection_id,
        "actions": ["ACTIVATE_GREEN_WAVE", "OVERRIDE_SIGNAL_CONTROL"],
        "active_weights": weights,
        "priority_level": "MAXIMUM"
    }
