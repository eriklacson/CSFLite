# Command line tool for converting Nuclie Scan to CSF Subcategories

import argparse
import os
import sys

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Local Helper Modules
import tools.global_helpers as global_helpers
import tools.nuclei_helpers as nuclei_helpers
import tools.nuclei_json_converter as nuclei_json_converter  # noqa: F401


def main():
    parser = argparse.ArgumentParser(description="CSFLite Nuclei Scan Tool")

    # Define command-line arguments
    parser.add_argument("--profile", type=str, help="scan profile to use", default="baseline_web")
    parser.add_argument("--targets", type=str, help="list of target assets for scanning", default="data/targets.txt")

    args = parser.parse_args()

    # get file paths from config file
    paths = global_helpers.get_paths()

    """ get CLI arguments"""
    # scan profile
    scan_profile_arg = args.profile
    scan_targets_arg = args.targets

    # load profiles.yaml
    print("\nGet profiles_set:\n")
    profiles = nuclei_helpers.load_profiles(paths["nuclei_profile"])
    print(profiles)

    # get profile definition
    print("\nGet specific profile:\n")
    print("Profile: " + args.profile)
    scan_profile = nuclei_helpers.get_profile(profiles, scan_profile_arg, allow_null=True)
    print(scan_profile)

    # sanity check - build nuclei command from profile
    print("\nBuild nuclei command from profile:\n")
    cmd = nuclei_helpers.build_nuclei_cmd(scan_profile, scan_targets_arg)
    print(cmd)


"""
    print("\nNuclei command string:\n")
    cmd_string = " ".join(cmd)
    print(cmd_string)

    nuclei_helpers.run_nuclei(cmd_string)
"""


if __name__ == "__main__":
    main()
