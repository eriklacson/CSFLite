#!/usr/bin/env python3
"""
nuclei_profiles.py — helpers for building nuclei commands from profiles.yml
"""

from __future__ import annotations
import os  # noqa: F401
import yaml
from typing import Any, Dict


def load_profile(profile_path: str) -> Dict[str, Any]:
    """Load profiles from a YAML file."""
    with open(profile_path, "r") as file:
        profiles = yaml.safe_load(file)
    return profiles
