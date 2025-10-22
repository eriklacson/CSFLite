# Command line tool for converting Nuclie Scan to CSF Subcategories

import os
import sys

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Local Helper Modules
import tools.global_helpers as global_helpers
import tools.nuclei_helpers as nuclei_helpers
import tools.nuclei_json_converter as nuclei_json_converter


def main():
    paths = global_helpers.get_paths()

    # sanity check - load profiles
    print("\nGet profiles_set:\n")
    profiles = nuclei_helpers.load_profiles(paths["nuclei_profile"])
    print(profiles)

    # sanity check - get specific profile
    print("\nGet specific profile:\n")
    baseline_web = nuclei_helpers.get_profile(profiles, "baseline_web", allow_null=True)
    print(baseline_web)

    # sanity check - build nuclei command from profile
    print("\nBuild nuclei command from profile:\n")
    cmd = nuclei_helpers.build_nuclei_cmd(baseline_web, "data/targets.txt")
    print(cmd)

    cmd_string = " ".join(cmd)
    print(cmd_string)

    results = nuclei_json_converter.convert_nuclei_raw_file("../scans/juice_shop_baseline_web.json")

    global_helpers.write_to_json(results, paths["nuclei_scan_findings"])


if __name__ == "__main__":
    main()
