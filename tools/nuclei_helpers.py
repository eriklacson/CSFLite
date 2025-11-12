#!/usr/bin/env python3
"""
nuclei_profiles.py — helpers for building nuclei commands from profiles.yml
"""

from __future__ import annotations

import os  # noqa: F401
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

import yaml

# Type alias for command representation
Command = Union[str, Iterable[str]]

PROJECT_ROOT = Path(__file__).resolve().parent.parent


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


def _resolve_targets_path(targets: str) -> str:
    """Resolve nuclei targets to an absolute filesystem path."""

    target_path = Path(targets)
    candidate_paths = []

    if target_path.is_absolute():
        candidate_paths.append(target_path)
    else:
        candidate_paths.append((Path.cwd() / target_path).resolve())
        candidate_paths.append((PROJECT_ROOT / target_path).resolve())

    for candidate in candidate_paths:
        if candidate.exists():
            return str(candidate)

    searched = ", ".join(str(path) for path in candidate_paths) or str(target_path)
    raise FileNotFoundError(f"Targets file '{targets}' was not found. Checked the following locations: {searched}.")


def _resolve_output_path(profile_output: str, scan_directory: Optional[str]) -> Path:
    """Resolve the nuclei output path taking into account optional scan directory overrides."""

    output_path = Path(profile_output)

    if scan_directory:
        output_dir = Path(scan_directory)
        if not output_dir.is_absolute():
            output_dir = (Path.cwd() / output_dir).resolve()
        return (output_dir / output_path.name).resolve()

    if output_path.is_absolute():
        return output_path.resolve()

    return (PROJECT_ROOT / output_path).resolve()


def build_nuclei_cmd(
    profile: dict,
    targets: str,
    output_path: Optional[str] = None,
    *,
    scan_directory: Optional[str] = None,
) -> List[str]:
    """
    Build a nuclei command string based on the base command and profile settings.
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

    # Use the provided output_path parameter or fallback to the profile's output setting
    profile_output = output_path or profile.get("output", "scans/nuclei_raw_scan.jsonl")

    # normalize important filesystem paths
    resolved_targets = _resolve_targets_path(targets)
    resolved_output_path = _resolve_output_path(profile_output, scan_directory)

    # ensure output directory exists - default to current directory if none specified
    # and create directory

    output_dir = resolved_output_path.parent
    os.makedirs(output_dir, exist_ok=True)

    """build the command string"""
    # base nuclei command
    cmd: List[str] = ["nuclei", "-l", resolved_targets]

    # add profile settings to the command
    if profile.get("input_mode"):
        cmd += ["-im", profile["input_mode"]]
    if tags:
        cmd += ["-tags", ",".join(map(str, tags))]
    if severity:
        cmd += ["-s", ",".join(map(str, severity))]

    # sane throttles
    cmd += ["-rl", str(rate_limit), "-c", str(concurrency), "-retries", str(retries), "-timeout", str(timeout)]

    # CSFLite expects JSONL output
    cmd += ["-omit-raw", "-jle", str(resolved_output_path)]

    return cmd


def _emit_stderr(message: Optional[str]) -> None:
    """Write stderr output to the active stderr stream."""

    if not message:
        return

    if not message.endswith("\n"):
        message = f"{message}\n"

    sys.stderr.write(message)
    sys.stderr.flush()


def _normalize_command(cmd: Command) -> List[str]:
    """Convert a nuclei command into the argv list expected by subprocess."""

    if isinstance(cmd, str):
        return shlex.split(cmd)

    if isinstance(cmd, Iterable):
        argv = list(cmd)
        if not all(isinstance(arg, str) for arg in argv):
            raise TypeError("Command arguments must be strings")
        return argv

    raise TypeError("Command must be a string or an iterable of arguments")


def run_nuclei(cmd: Command, timeout: int = None) -> subprocess.CompletedProcess:
    """Run the nuclei CLI using a command string or iterable of arguments.

    nuclei writes JSON to file so stdout is not captured; stderr is piped so errors
    are surfaced to the caller.
    """
    argv = _normalize_command(cmd)

    try:
        result = subprocess.run(  # noqa: S603
            argv,
            check=True,
            timeout=timeout,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError as error:
        command_display = cmd if isinstance(cmd, str) else " ".join(argv)
        raise RuntimeError(
            f"Failed to execute nuclei command '{command_display}'. "
            "Ensure nuclei is installed and available on the PATH."
        ) from error
    except subprocess.CalledProcessError as error:
        _emit_stderr(error.stderr)
        raise

    _emit_stderr(result.stderr)
    return result
