from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from flow_guardian_x.perception.preprocessing import Preprocessor
from flow_guardian_x.perception.feature_engineering import FeatureEngineer
from flow_guardian_x.prediction.model_inference import ModelInference
from flow_guardian_x.state_estimation.regime_classifier import RegimeClassifier
from flow_guardian_x.risk_engine.bottleneck_risk import BottleneckRisk

router = APIRouter(tags=["Prediction"])

class TrafficInput(BaseModel):
    vehicle_count: int
    avg_speed_kmph: float
    road_capacity: int
    rainfall_intensity: float = 0.0
    accident_flag: bool = False

# Initialize modules
preprocessor = Preprocessor()
engineer = FeatureEngineer()
inference = ModelInference()
classifier = RegimeClassifier()
risk_engine = BottleneckRisk()

@router.post("/predict")
def predict_traffic(data: TrafficInput):
    # Create a DataFrame for processing
    input_data = pd.DataFrame([{
        "vehicle_count": data.vehicle_count,
        "avg_speed_kmph": data.avg_speed_kmph,
        "road_capacity": data.road_capacity,
        "rainfall_intensity": data.rainfall_intensity,
        "accident_flag": data.accident_flag,
        "day_of_week": "Monday", # Default context
        "hour_of_day": 12        # Default context
    }])

    # 1. Preprocess & Feature Engineering
    # Note: Preprocessor might need fitted scaler, using basic transform for now or fallback
    features = engineer.engineer_features(input_data).iloc[0].to_dict()

    # 2. Predict Delay
    predicted_delay = inference.get_prediction(features)

    # 3. Classify Regime
    regime = classifier.classify(
        features.get('vehicle_density', 0.5),
        features.get('speed_drop_index', 0),
        0.05 # Default violation rate
    )

    # 4. Calculate Risk
    risk_score = risk_engine.calculate_risk(
        features.get('vehicle_density', 0.5),
        0.1, # signal penalty
        0.05 # violation rate
    )

    return {
        "predicted_delay_minutes": round(float(predicted_delay[0]) if isinstance(predicted_delay, (list, pd.Series)) else float(predicted_delay), 2),
        "congestion_regime": regime,
        "bottleneck_risk_score": round(float(risk_score), 2),
        "emission_load": round(float(features.get('total_emission_level', 0)), 2)
    }
