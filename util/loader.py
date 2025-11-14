# util/loader.py
import yaml
import json
from pathlib import Path
from typing import List, Any


# Load the process configuration (YAML)
def load_config(path: str = "configs/process.yaml") -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


# Load a sequence of input values (JSON)
def load_inputs(path: str = "data/inputs.json") -> List[Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # Basic validation
    if "pressures" not in data or not isinstance(data["pressures"], list):
        raise ValueError("JSON must contain a 'pressures' array (list).")
    return data["pressures"]
