def calculate_weather_penalty(rainfall_intensity):
    """Adds penalty based on rainfall intensity (0.0 to 1.0)."""
    # Max rainfall intensity assumed to be around 50 mm/h for normalization
    penalty = rainfall_intensity / 50.0
    return min(penalty, 1.0)
