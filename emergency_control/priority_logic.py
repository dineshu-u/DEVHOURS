from flow_guardian_x.decision_engine.weight_adapter import WeightAdapter

class PriorityLogic:
    @staticmethod
    def get_priority_weights():
        """Overrides normal routing weights to prioritize delay minimization."""
        return WeightAdapter.get_weights(is_emergency=True)
