class ShockwaveDetector:
    def __init__(self, threshold=15):
        self.previous_speed = None
        self.threshold = threshold

    def detect_shockwave(self, current_speed):
        """Detects backward-moving braking waves by comparing speeds."""
        if self.previous_speed is None:
            self.previous_speed = current_speed
            return False
        
        # If speed drops significantly between timesteps
        speed_delta = self.previous_speed - current_speed
        self.previous_speed = current_speed
        
        return speed_delta > self.threshold
