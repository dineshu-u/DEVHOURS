from flow_guardian_x.config import CRITICAL_DENSITY_DEFAULT

class RegimeClassifier:
    def __init__(self, critical_density=CRITICAL_DENSITY_DEFAULT):
        self.critical_density = critical_density

    def classify(self, density, speed_drop, violation_rate):
        """
        Classifies traffic into:
        - Free Flow
        - Stable Flow
        - Unstable Flow
        - Gridlock Risk
        """
        # Mathematical boundaries
        if density < 0.2 * self.critical_density:
            return "Free Flow"
        elif density < 0.6 * self.critical_density:
            return "Stable Flow"
        elif density < self.critical_density:
            return "Unstable Flow"
        else:
            # High density + high violation rate or high speed drop indicates gridlock risk
            if violation_rate > 0.3 or speed_drop > 50:
                return "Gridlock Risk"
            return "Unstable Flow"
