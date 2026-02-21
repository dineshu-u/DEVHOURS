from flow_guardian_x.config import BOTTLENECK_RISK_THRESHOLD

class EscalationDetector:
    @staticmethod
    def detect_escalation(risk_score, weather_penalty, accident_penalty, speed_drop):
        """
        Flag Bottleneck Escalation Risk if:
        Speed_Drop_Index > Threshold AND Accident_Penalty + Weather_Penalty > X
        """
        combined_penalty = weather_penalty + accident_penalty
        
        # Using thresholds from config
        if speed_drop > 30 and combined_penalty > 0.5:
            return True
            
        if risk_score > BOTTLENECK_RISK_THRESHOLD:
            return True
            
        return False
