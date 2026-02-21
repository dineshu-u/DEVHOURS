from flow_guardian_x.emergency_control.priority_logic import PriorityLogic
from flow_guardian_x.config import EMERGENCY_ALPHA

def test_emergency_weights():
    weights = PriorityLogic.get_priority_weights()
    # EMERGENCY_ALPHA should be 0.9 as per config
    assert weights[0] == 0.9
    assert weights[1] < weights[0]
    assert weights[2] < weights[0]
