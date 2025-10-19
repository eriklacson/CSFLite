import json
from pathlib import Path


# test get_paths function
def test_get_paths():
    from tools.global_helpers import get_paths

    config_path = Path(__file__).resolve().parent.parent / "config" / "path_config.json"

    with open(config_path, encoding="utf-8") as config_file:
        expected_paths = json.load(config_file)

    assert get_paths() == expected_paths
