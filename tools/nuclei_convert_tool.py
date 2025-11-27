#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to convert Nuclei JSON output to a simplified summary format.
"""

import argparse
import logging
import sys

from tools.nuclei_json_converter import convert_nuclei_raw_file


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Convert Nuclei JSON output to a simplified format.")
    parser.add_argument("input_file", type=str, help="Path to the Nuclei JSON file to be converted.")

    parser.add_argument("output_file", type=str, help="Path to save the converted output file.")
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()

    try:
        # Convert the Nuclei JSON file
        converted_data = convert_nuclei_raw_file(args.input_file)
        print(converted_data)
    except Exception as e:
        logging.error("An error occurred during conversion: %s", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
