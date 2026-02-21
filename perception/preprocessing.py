import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

class Preprocessor:
    def __init__(self):
        self.scalers = {}
        self.label_encoders = {}
        self.categorical_cols = ['weather', 'road_type', 'road_condition', 'vehicle_type']
        self.numeric_cols = [
            'vehicle_count', 'avg_speed_kmph', 'road_capacity', 
            'signal_cycle_time_sec', 'emergency_vehicle_count', 
            'vehicle_emission_rate_g_per_km', 'violation_vehicle_count', 
            'rainfall_intensity'
        ]

    def handle_missing_values(self, df):
        """Fill missing values with median for numeric and mode for categorical."""
        df = df.copy()
        for col in self.numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        
        for col in self.categorical_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].mode()[0])
        return df

    def encode_categorical(self, df, fit=False):
        """Encode categorical variables using Label Encoding."""
        df = df.copy()
        for col in self.categorical_cols:
            if col in df.columns:
                if fit:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    if col in self.label_encoders:
                        df[col] = self.label_encoders[col].transform(df[col].astype(str))
        return df

    def normalize_numeric(self, df, fit=False):
        """Scale numeric features."""
        df = df.copy()
        for col in self.numeric_cols:
            if col in df.columns:
                if fit:
                    self.scalers[col] = StandardScaler()
                    df[[col]] = self.scalers[col].fit_transform(df[[col]])
                else:
                    if col in self.scalers:
                        df[[col]] = self.scalers[col].transform(df[[col]])
        return df

    def transform(self, df, fit=False):
        """Full preprocessing pipeline."""
        df = self.handle_missing_values(df)
        df = self.encode_categorical(df, fit=fit)
        # We might not always want to normalize if we are doing feature engineering first
        return df
