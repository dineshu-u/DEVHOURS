import pandas as pd
import json
import os
from flow_guardian_x.config import DATA_RAW_PATH

class DataLoader:
    @staticmethod
    def load_from_excel(file_path=None):
        """Loads traffic data from Excel file."""
        path = file_path or DATA_RAW_PATH
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset not found at {path}")
        return pd.read_excel(path)

    @staticmethod
    def load_from_json(json_data):
        """Converts incoming JSON request to pandas DataFrame."""
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        
        # If it's a single record, wrap in a list
        if isinstance(json_data, dict):
            json_data = [json_data]
            
        return pd.DataFrame(json_data)

    @staticmethod
    def load_sample_scenario(scenario_name):
        """Loads a specific scenario from the scenarios folder."""
        path = f"data/scenarios/{scenario_name}.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Scenario {scenario_name} not found.")
        with open(path, 'r') as f:
            return DataLoader.load_from_json(json.load(f))
