class ObjectiveFunction:
    @staticmethod
    def calculate_cost(predicted_delay, emission_load, bottleneck_risk, alpha, beta, gamma):
        """
        Objective = alpha(Predicted_Delay) + beta(Emission_Load) + gamma(Bottleneck_Risk)
        """
        # Normalize inputs if necessary (assuming they are already scaled or consistent)
        cost = (alpha * predicted_delay) + (beta * emission_load) + (gamma * bottleneck_risk)
        return cost
