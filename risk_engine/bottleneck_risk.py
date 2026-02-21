class BottleneckRisk:
    @staticmethod
    def calculate_base_risk(density, signal_penalty, violation_rate):
        """Computes risk score using density, signal delay, and violations."""
        # Simple weighted sum for risk
        risk_score = (density * 0.5) + (signal_penalty * 0.3) + (violation_rate * 0.2)
        return min(risk_score, 1.0)
