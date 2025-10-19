import json
from pathlib import Path


def get_paths():
    """Return the paths for input, reference, and output datasets."""

    config_path = Path(__file__).resolve().parent.parent / "config" / "path_config.json"

    with open(config_path, encoding="utf-8") as config_file:
        return json.load(config_file)
