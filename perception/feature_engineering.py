import pandas as pd
from flow_guardian_x.config import FREE_FLOW_SPEED

class FeatureEngineer:
    @staticmethod
    def engineer_features(df):
        """Creates derived features based on project specifications."""
        df = df.copy()
        
        # 1. Vehicle Density: vehicle_count / road_capacity
        if 'vehicle_count' in df.columns and 'road_capacity' in df.columns:
            df['vehicle_density'] = df['vehicle_count'] / df['road_capacity']
        
        # 2. Speed Drop Index: Free Flow Speed (80) - avg_speed_kmph
        if 'avg_speed_kmph' in df.columns:
            df['speed_drop_index'] = FREE_FLOW_SPEED - df['avg_speed_kmph']
        
        # 3. Violation Rate: violation_vehicle_count / vehicle_count
        if 'violation_vehicle_count' in df.columns and 'vehicle_count' in df.columns:
            # Handle division by zero
            df['violation_rate'] = df['violation_vehicle_count'] / df['vehicle_count'].replace(0, 1)
        
        # 4. Emission Load: vehicle_count * vehicle_emission_rate_g_per_km
        if 'vehicle_count' in df.columns and 'vehicle_emission_rate_g_per_km' in df.columns:
            df['total_emission_level'] = df['vehicle_count'] * df['vehicle_emission_rate_g_per_km']
        
        # Penalties (if not already in dataset, we can derive simple placeholders)
        if 'accident_flag' in df.columns:
            df['accident_penalty'] = df['accident_flag'] * 50 # Example penalty
            
        if 'rainfall_intensity' in df.columns:
            df['weather_penalty'] = df['rainfall_intensity'] * 10 # Example penalty
            
        return df
