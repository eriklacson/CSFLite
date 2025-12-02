#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to convert Nuclei JSON output to a simplified summary format.
"""

import os
import sys

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tools.global_helpers as global_helpers
import tools.nuclei_json_converter as converter


def main():
    """Main function."""
    converted_data = converter.convert_nuclei_raw_file("../scans/nuclei_inventory.json")
    print(converted_data)
    global_helpers.write_to_json(converted_data, "../output/nuclei_inventory_converted.json")


if __name__ == "__main__":
    sys.exit(main())
