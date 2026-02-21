import pandas as pd

def calculate_density(vehicle_count, road_capacity):
    """Computes density = vehicle_count / road_capacity"""
    if road_capacity <= 0:
        return 0
    return vehicle_count / road_capacity

def calculate_flow(vehicle_count, avg_speed):
    """Computes basic flow (vehicles passing point per hour)"""
    return vehicle_count * avg_speed
