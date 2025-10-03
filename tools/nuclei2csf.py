# Command line too for converting Nuclie Scan to CSF Subcategories

import os
import sys

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Local Helper Module
import tools.assess as assess
import tools.nuclei_helpers as nuclei_helpers


def main():
    paths = assess.get_paths()
    profiles = nuclei_helpers.load_profiles(paths["nuclei_profile"])

    print(profiles)

    print("\nGet specific profile:\n")

    baseline_web = nuclei_helpers.get_profile(profiles, "web", allow_null=True)
    print(baseline_web)


if __name__ == "__main__":
    main()
