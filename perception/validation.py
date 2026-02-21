import pandas as pd

class Validator:
    @staticmethod
    def validate_input(df):
        """Checks for data integrity and realistic limits."""
        issues = []
        
        # Check for negative values
        cols_to_check_positive = ['vehicle_count', 'avg_speed_kmph', 'road_capacity', 'rainfall_intensity']
        for col in cols_to_check_positive:
            if col in df.columns:
                if (df[col] < 0).any():
                    issues.append(f"Negative values detected in {col}")
        
        # Check road capacity > 0
        if 'road_capacity' in df.columns:
            if (df['road_capacity'] <= 0).any():
                issues.append("Road capacity must be greater than zero")
                
        # Check speed limits (realistic max 200 kmph)
        if 'avg_speed_kmph' in df.columns:
            if (df['avg_speed_kmph'] > 200).any():
                issues.append("Unrealistically high average speed detected (>200 kmph)")
                
        if issues:
            raise ValueError("Data validation failed: " + "; ".join(issues))
            
        return True
