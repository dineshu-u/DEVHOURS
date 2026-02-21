from flow_guardian_x.simulation.traffic_generator import TrafficGenerator

class ScenarioRunner:
    @staticmethod
    def run_rush_hour():
        """Simulates rush hour (high volume, low speed)."""
        return TrafficGenerator.generate_record(road_capacity=1000)

    @staticmethod
    def run_emergency():
        """Simulates emergency vehicle scenario."""
        record = TrafficGenerator.generate_record()
        record['emergency_vehicle_count'] = 1
        record['avg_speed_kmph'] = 20
        return record
