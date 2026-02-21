import numpy as np
import pandas as pd
from flow_guardian_x.config import CRITICAL_DENSITY_DEFAULT

def estimate_critical_density(df):
    """
    Analyzes dataset and estimates the density where speed sharply collapses.
    If not enough data, returns default from config.
    """
    if 'vehicle_density' not in df.columns or 'avg_speed_kmph' not in df.columns:
        return CRITICAL_DENSITY_DEFAULT
    
    # Simple estimation: point where speed drops below 50% of free flow speed
    # Free flow speed is 80 (from config)
    threshold_speed = 40 
    
    # Sort by density
    df_sorted = df.sort_values('vehicle_density')
    
    # Find the first density where speed drops below threshold
    congested = df_sorted[df_sorted['avg_speed_kmph'] < threshold_speed]
    
    if congested.empty:
        return CRITICAL_DENSITY_DEFAULT
    
    return congested['vehicle_density'].iloc[0]
