from flow_guardian_x.prediction.delay_regression import DelayPredictor
from flow_guardian_x.prediction.nonlinear_model import NonlinearDelayModel

class ModelInference:
    def __init__(self):
        self.predictor = DelayPredictor()
        self.predictor.load_model()
        self.nonlinear_predictor = NonlinearDelayModel()

    def get_prediction(self, feature_dict, use_nonlinear=False):
        """Predicts delay for a single record or list of records."""
        if use_nonlinear:
            density = feature_dict.get('vehicle_density', 0.5)
            return self.nonlinear_predictor.calculate_predicted_delay(density)
            
        return self.predictor.predict(feature_dict)
