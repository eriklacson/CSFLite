# Command line too for converting Nuclie Scan to CSF Subcategories

import json


# Local Helper Module
from nuclei_helpers import load_profiles  # noqa: F401
from assess import get_paths  # noqa: F401


def main():
    paths = get_paths()
    profile = load_profiles(paths["nuclei_profile"])

    print(json.dumps(profile, indent=4))


if __name__ == "__main__":
    main()
