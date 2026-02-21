class PolicyManager:
    @staticmethod
    def decide_action(regime, escalation_risk, is_emergency):
        """Chooses what the system should do."""
        actions = []
        
        if is_emergency:
            actions.append("TRIGGER_EMERGENCY_PRIORITY")
            actions.append("ACTIVATE_GREEN_WAVE")
            
        if escalation_risk:
            actions.append("TRIGGER_BOTTLENECK_ALERT")
            actions.append("DENSE_TRAFFIC_REROUTE")
            
        if regime == "Gridlock Risk":
            actions.append("MANDATORY_DIVERSION")
            
        if not actions:
            actions.append("CONTINUE_NORMAL_OPERATION")
            
        return actions
