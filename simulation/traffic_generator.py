import random

class TrafficGenerator:
    @staticmethod
    def generate_record(road_capacity=1000):
        """Generates a random traffic record."""
        vehicle_count = random.randint(100, 1200)
        avg_speed = random.uniform(10, 80)
        
        return {
            "vehicle_count": vehicle_count,
            "avg_speed_kmph": avg_speed,
            "road_capacity": road_capacity,
            "weather": random.choice(["Sunny", "Overcast", "Rainy"]),
            "accident_flag": random.random() < 0.05, # 5% chance of accident
            "rainfall_intensity": random.uniform(0, 50) if random.random() < 0.2 else 0,
            "emergency_vehicle_count": random.randint(0, 2) if random.random() < 0.1 else 0,
            "vehicle_emission_rate_g_per_km": random.uniform(100, 300)
        }
