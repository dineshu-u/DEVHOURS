from collections import deque

class StateTracker:
    def __init__(self, history_size=5):
        self.state_history = deque(maxlen=history_size)

    def update_state(self, current_regime):
        """Adds current regime to history and detects transitions."""
        self.state_history.append(current_regime)

    def detect_instability(self):
        """Detects if traffic is moving from Stable to Unstable/Gridlock."""
        if len(self.state_history) < 2:
            return False
        
        # Check for rapid deterioration
        states = list(self.state_history)
        if states[-2] == "Stable Flow" and states[-1] in ["Unstable Flow", "Gridlock Risk"]:
            return True
        return False
