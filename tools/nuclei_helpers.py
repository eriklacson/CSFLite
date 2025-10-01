#!/usr/bin/env python3
"""
nuclei_profiles.py — helpers for building nuclei commands from profiles.yml
"""

from __future__ import annotations
import os  # noqa: F401
import yaml
from typing import Any, Dict


def load_profiles(profile_path: str) -> Dict[str, Any]:
    """Load profiles from a YAML file."""
    with open(profile_path, "r") as file:
        profiles = yaml.safe_load(file)

    """return the profiles dictionary"""
    return profiles


def get_profile(profiles: dict, profile: str, default=None, allow_null=False):
    """
    Retrieve a specific profile from profiles dict using the profile name,
    """

    if not isinstance(profiles, dict):
        raise TypeError("Expected a dictionary as 'data'.")

    if profile not in profiles:
        return default

    profile = profiles[profile]

    if profile is None and not allow_null:
        return default

    return profile
