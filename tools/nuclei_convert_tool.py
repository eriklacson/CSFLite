#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to convert Nuclei JSON output to a simplified summary format.
"""

import argparse
import os
import sys
from typing import Iterable, Optional

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tools.global_helpers as global_helpers
import tools.nuclei_json_converter as converter


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    """Parse command line arguments for the Nuclei scanning CLI."""

    parser = argparse.ArgumentParser(description="CSFLite Nuclei output converter")
    parser.add_argument("--nuclei_raw", type=str, help="Output JSON file from Nuclei")
    parser.add_argument("--csflite_out", type=str, help="CSFLite JSON file")
    return parser.parse_args(argv)


def validate_arguments(args: argparse.Namespace) -> None:
    """Validate that both arguments are provided."""
    if not args.nuclei_raw or not args.csflite_out:
        raise ValueError("Both '--nuclei_raw' and '--csflite_out' arguments are required.")


def main(argv: Optional[Iterable[str]] = None) -> None:
    try:
        args = parse_args(argv)

        # Validate the arguments
        validate_arguments(args)

        nuclei_raw_arg = args.nuclei_raw
        csflite_out_arg = args.csflite_out

        converted_data = converter.convert_nuclei_raw_file(nuclei_raw_arg)
        print(converted_data)
        global_helpers.write_to_json(converted_data, csflite_out_arg)

    except ValueError as ve:
        print(f"Argument Error: {ve}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
