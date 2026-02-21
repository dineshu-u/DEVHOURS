import pytest
from flow_guardian_x.prediction.delay_regression import DelayPredictor

def test_delay_prediction_fallback():
    predictor = DelayPredictor()
    # Mock features
    features = {'vehicle_density': 0.8, 'speed_drop_index': 50}
    prediction = predictor.predict(features)
    
    # (0.8 * 10) + (50 * 0.2) = 8 + 10 = 18
    assert prediction == 18.0

def test_delay_prediction_low_traffic():
    predictor = DelayPredictor()
    features = {'vehicle_density': 0.1, 'speed_drop_index': 5}
    prediction = predictor.predict(features)
    
    # (0.1 * 10) + (5 * 0.2) = 1 + 1 = 2
    assert prediction == 2.0
