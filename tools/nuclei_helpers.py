#!/usr/bin/env python3
"""
nuclei_profiles.py — helpers for building nuclei commands from profiles.yml
"""

from __future__ import annotations

import os  # noqa: F401
import subprocess
from typing import Any, Dict, List

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


def build_nuclei_cmd(profile: dict, targets: str) -> str:
    """
    build a nuclei command string based on the base command and profile settings.
    """

    """parameter validation"""
    # validate profile is a dict
    if not isinstance(profile, dict):
        raise TypeError("Expected a dictionary as 'profile'")

    if targets is None or targets.strip() == "":
        raise ValueError("A valid target must be provided")

    """prepare command components"""

    # Extract profile settings with defaults
    tags = profile.get("tags", [])  # noqa: F841
    severity = profile.get("severity", [])  # noqa: F841
    rate_limit = profile.get("rate_limit", 3)  # noqa: F841
    concurrency = profile.get("concurrency", 2)  # noqa: F841
    retries = profile.get("retries", 2)  # noqa: F841
    timeout = profile.get("timeout", 5)  # noqa: F841
    output_path = profile.get("output", "data/nuclei_raw.jsonl")  # noqa: F841
    input_mode = profile.get("input_mode")  # noqa: F841

    # insure output directory exists - default to current directory if none specified
    # and create directory
    output_path = os.path.dirname(output_path) or "."
    os.makedirs(output_path, exist_ok=True)

    """build the command string"""
    # base nuclei command
    cmd: List[str] = ["nuclei", "-l", targets]

    # add profile settings to the command
    if input_mode:
        cmd += ["-im", input_mode]
    if tags:
        cmd += ["-tags", ",".join(map(str, tags))]
    if severity:
        cmd += ["-s", ",".join(map(str, severity))]

    # sane throttles
    cmd += ["-rl", str(rate_limit), "-c", str(concurrency), "-retries", str(retries), "-timeout", str(timeout)]

    # CSFLite expects JSONL output
    cmd += ["-jle", output_path]

    return cmd


def run_nuclei(cmd: List[str], timeout: int = None) -> subprocess.CompletedProcess:
    """
    launch the nuclei process and wait for it to finish.
    nuclei writes JSON to file so output is not captured. pipe stderr to surface errors.
    """
    return subprocess.run(cmd, check=True, timeout=timeout)  # noqa: S603
