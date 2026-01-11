import yaml
import os

def load_config(config_path="config/config.yaml"):
    """Load configuration from a YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
        
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

# Load once to be imported elsewhere
config = load_config()
