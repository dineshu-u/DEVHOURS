from flow_guardian_x.config import CRITICAL_DENSITY_DEFAULT

class NonlinearDelayModel:
    """
    Implements Nonlinear Delay Growth for non-historical events.
    Formula: Delay ∝ Vehicle_Density / (1 - (Vehicle_Density / Critical_Density))
    """
    def __init__(self, critical_density=CRITICAL_DENSITY_DEFAULT):
        self.critical_density = critical_density

    def calculate_predicted_delay(self, density, base_delay=1.0):
        """
        Calculates delay using the nonlinear congestion model.
        As density approaches critical_density, delay grows exponentially.
        """
        # Ensure density doesn't exceed 99% of critical to avoiding division by zero/negative
        safe_density = min(density, self.critical_density * 0.99)
        
        # Scaling factor to align with real-world minutes
        growth_factor = safe_density / (1 - (safe_density / self.critical_density))
        
        # Multiply by a base constant (e.g., 5 mins base)
        predicted_delay = base_delay * growth_factor
        
        return round(max(predicted_delay, 0), 2)
