import json
import os

def load_json(file_path, default_value=None):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return default_value

def save_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)