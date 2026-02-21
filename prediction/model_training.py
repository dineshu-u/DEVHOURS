import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from flow_guardian_x.config import MODEL_SAVE_PATH

class ModelTrainer:
    def __init__(self):
        self.features = [
            'vehicle_density', 'speed_drop_index', 'violation_rate', 
            'weather_penalty', 'accident_penalty', 'road_capacity'
        ]
        self.target = 'delay_minutes'
        
        if not os.path.exists(MODEL_SAVE_PATH):
            os.makedirs(MODEL_SAVE_PATH)

    def train(self, df):
        """Trains both Linear Regression and Random Forest models and compares them."""
        X = df[self.features]
        y = df[self.target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Linear Regression
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        
        # Random Forest
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        
        # Save the best model (using RF by default for now)
        joblib.dump(rf_model, os.path.join(MODEL_SAVE_PATH, 'delay_regression_model.pkl'))
        
        return lr_model, rf_model, X_test, y_test
