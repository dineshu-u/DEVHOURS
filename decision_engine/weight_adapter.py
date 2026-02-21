from flow_guardian_x.config import (
    DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA,
    EMERGENCY_ALPHA, EMERGENCY_BETA, EMERGENCY_GAMMA
)

class WeightAdapter:
    @staticmethod
    def get_weights(is_emergency=False, is_rainy=False):
        """Dynamically changes weights depending on condition."""
        if is_emergency:
            return EMERGENCY_ALPHA, EMERGENCY_BETA, EMERGENCY_GAMMA
        
        if is_rainy:
            # In rain, maybe prioritize safety (bottleneck risk) slightly more
            return 0.5, 0.2, 0.3
            
        return DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA
