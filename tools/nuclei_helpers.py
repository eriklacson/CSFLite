#!/usr/bin/env python3
"""
nuclei_profiles.py — helpers for building nuclei commands from profiles.yml
"""

from __future__ import annotations

import os  # noqa: F401
from typing import Any, Dict

import yaml


def load_profiles(profile_path: str) -> Dict[str, Any]:
    """Load profiles from a YAML file."""
    with open(profile_path, "r") as file:
        profiles = yaml.safe_load(file)

    """return the profiles dictionary"""
    return profiles


def get_profile(profiles_data: dict, profile_name: str, default=None, allow_null=False):
    """
    Retrieve a specific profile from profiles dict using the profile name,
    """

    if not isinstance(profiles_data, dict):
        raise TypeError("Expected a dictionary as 'data'.")

    profiles = profiles_data.get("profiles", {})

    if profile_name not in profiles:
        return default

    profile = profiles.get(profile_name)

    if profile is None and not allow_null:
        return default

    return profile
