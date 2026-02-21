from flow_guardian_x.config import FREE_FLOW_SPEED

def analyze_speed_drop(avg_speed):
    """Computes speed drop and flags abnormal deceleration."""
    drop = FREE_FLOW_SPEED - avg_speed
    is_abnormal = drop > 40 # Threshold for sudden drop
    return drop, is_abnormal
