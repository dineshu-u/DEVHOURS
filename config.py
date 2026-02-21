# Flow Guardian X - Central Configuration

# Traffic Physics Constants
FREE_FLOW_SPEED = 80  # kmph
CRITICAL_DENSITY_DEFAULT = 0.5  # Critical density (vehicles per unit capacity) where speed collapses

# Routing Weights (Multi-Objective Optimization)
# Objective = alpha * Predicted_Delay + beta * Emission_Load + gamma * Bottleneck_Risk
DEFAULT_ALPHA = 0.6  # Weight for Predicted Delay
DEFAULT_BETA = 0.2   # Weight for Emission Load
DEFAULT_GAMMA = 0.2  # Weight for Bottleneck Risk

# Emergency Override Weights
# When emergency=True, prioritize delay reduction heavily
EMERGENCY_ALPHA = 0.9
EMERGENCY_BETA = 0.05
EMERGENCY_GAMMA = 0.05

# Risk Engine Thresholds
BOTTLENECK_RISK_THRESHOLD = 0.7  # Above this, flag bottleneck escalation
SPEED_DROP_THRESHOLD = 30        # kmph drop speed threshold for risk flagging
ACCIDENT_WEATHER_PENALTY_THRESHOLD = 0.5 # Combined penalty threshold for escalation

import os

# Project Root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8080

# File Paths
DATA_RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "Flow_Guardian_Traffic_Dataset.xlsx")
DATA_PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_traffic_data.csv")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "prediction", "models")

# Ensure model directory exists
if not os.path.exists(MODEL_SAVE_PATH):
    os.makedirs(MODEL_SAVE_PATH)
