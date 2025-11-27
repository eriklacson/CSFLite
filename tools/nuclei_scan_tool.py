# Command line interface for configuring and running Nuclei scans for CSFLite mapping

import argparse
import os
import sys
from typing import Iterable, Optional

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Local Helper Modules
import tools.global_helpers as global_helpers
import tools.nuclei_helpers as nuclei_helpers
import tools.nuclei_json_converter as nuclei_json_converter  # noqa: F401


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    """Parse command line arguments for the Nuclei scanning CLI."""

    parser = argparse.ArgumentParser(description="CSFLite Nuclei Scan Tool")
    parser.add_argument("--profile", type=str, help="scan profile to use", default="baseline_web")
    parser.add_argument("--targets", type=str, help="list of target assets for scanning", default="data/targets.txt")
    parser.add_argument(
        "--scan-dir",
        type=str,
        dest="scan_directory",
        default=None,
        help="Directory where raw nuclei scan output files will be saved.",
    )

    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> None:
    args = parse_args(argv)

    # get file paths from config file
    paths = global_helpers.get_paths()

    scan_profile_arg = args.profile
    scan_targets_arg = args.targets

    # load profiles.yaml
    print("\nGet profiles_set:\n")
    profiles = nuclei_helpers.load_profiles(paths["nuclei_profile"])
    print(profiles)

    # get profile definition
    print("\nGet specific profile:\n")
    print(f"Profile: {scan_profile_arg}")
    scan_profile = nuclei_helpers.get_profile(profiles, scan_profile_arg, allow_null=True)
    print(scan_profile)

    # sanity check - build nuclei command from profile
    print("\nBuild nuclei command from profile:\n")
    cmd = nuclei_helpers.build_nuclei_cmd(
        scan_profile,
        scan_targets_arg,
        scan_directory=args.scan_directory,
    )
    print(cmd)

    print("\nNuclei command string:\n")
    cmd_string = " ".join(cmd)
    print(cmd_string)

    nuclei_helpers.run_nuclei(cmd_string)


if __name__ == "__main__":
    main()
