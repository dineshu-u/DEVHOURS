import joblib
import os
from flow_guardian_x.config import MODEL_SAVE_PATH

class DelayPredictor:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(MODEL_SAVE_PATH, 'delay_regression_model.pkl')

    def load_model(self):
        """Loads trained regression model from disk."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            print("Warning: Model file not found. Please train the model first.")

    def predict(self, features):
        """Predicts delay in minutes."""
        if self.model is None:
            # Fallback to a simple heuristic if model is not trained
            # Delay proportional to density and speed drop
            density = features.get('vehicle_density', 0)
            speed_drop = features.get('speed_drop_index', 0)
            return (density * 10) + (speed_drop * 0.2)
            
        return self.model.predict(features)
