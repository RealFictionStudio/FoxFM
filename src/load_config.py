import json

def load_config_settings(filename:str="config.json"):
    with open(filename, 'r') as f:
        config = json.loads(f.read())
        