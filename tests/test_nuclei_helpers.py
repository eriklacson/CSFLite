# Unit test for nuclei_helpers.py

# Standard Library Modules
import subprocess
from textwrap import dedent
from unittest.mock import mock_open, patch

import pytest  # noqa: F401

# Third-Party Modules
import yaml

# Local Helper Module
import tools.nuclei_helpers as nuclei_helpers


def test_load_profile_valid():
    """Test the load_profile function with a mock YAML file."""

    # Mock YAML content
    mock_yaml_content = dedent(
        """
    version: 1
    profiles:
      test_profile:
        tags: [test, mock]
        severity: [info]
        output: data/test_output.jsonl
    """
    )

    # Mock the open function and patch it in the context of the load_profiles function
    with patch("builtins.open", mock_open(read_data=mock_yaml_content)):
        # Call the function with a mock file path
        profiles = nuclei_helpers.load_profiles("mock_profiles.yaml")

        # Assertions
        assert profiles["version"] == 1, "Version mismatch in loaded profiles."
        assert "test_profile" in profiles["profiles"], "Profile 'test_profile' not found."
        assert profiles["profiles"]["test_profile"]["tags"] == ["test", "mock"], "Tags mismatch."
        assert profiles["profiles"]["test_profile"]["output"] == "data/test_output.jsonl", "Output path mismatch."
        assert profiles["profiles"]["test_profile"]["severity"] == ["info"], "Severity mismatch."


def test_load_profile_file_not_found():
    """Test load_profiles function when the file does not exist."""
    with pytest.raises(FileNotFoundError, match="No such file or directory"):
        nuclei_helpers.load_profiles("non_existent_file.yaml")


def test_load_profile_invalid_yaml():
    """Test load_profiles function with invalid YAML content."""
    mock_invalid_yaml_content = dedent(
        """
        version: 1
        profiles:
          test_profile:
            tags: [test, mock
            severity: [info]
            output: data/test_output.jsonl
        """
    )

    with patch("builtins.open", mock_open(read_data=mock_invalid_yaml_content)):
        with pytest.raises(yaml.YAMLError):  # Replace Exception with the specific exception type if known
            nuclei_helpers.load_profiles("mock_invalid_profiles.yaml")


"""test get_profile function"""

# set-up test data set


def test_get_profile_valid():
    """Test retrieving an existing profile."""

    profiles = {
        "version": 1,
        "profiles": {
            "test_profile": {
                "tags": ["test", "mock"],
                "severity": ["info"],
                "output": "data/test_output.jsonl",
            }
        },
    }

    result = nuclei_helpers.get_profile(profiles, "test_profile")

    assert result == {
        "tags": ["test", "mock"],
        "severity": ["info"],
        "output": "data/test_output.jsonl",
    }, "Failed to retrieve the correct profile."


def test_get_profile_missing():
    """Test retrieving a non-existent profile with a default value."""
    profiles = {
        "version": 1,
        "profiles": {
            "test_profile": {
                "tags": ["test", "mock"],
                "severity": ["info"],
                "output": "data/test_output.jsonl",
            }
        },
    }

    result = nuclei_helpers.get_profile(profiles, "missing_profile", default="default_value")
    assert result == "default_value", "Default value not returned for missing profile."


def test_get_profile_null_not_allowed():
    """Test retrieving a profile with None value when allow_null is False."""
    profiles = {
        "version": 1,
        "profiles": {
            "test_profile": {
                "tags": ["test", "mock"],
                "severity": ["info"],
                "output": "data/test_output.jsonl",
            }
        },
    }

    result = nuclei_helpers.get_profile(profiles, "no_profile", default="default_value", allow_null=False)
    assert result == "default_value", "Default value not returned when allow_null is False."


def test_get_profile_null_allowed():
    """Test retrieving a profile with None value when allow_null is True."""
    profiles = {
        "version": 1,
        "profiles": {
            "test_profile": {
                "tags": ["test", "mock"],
                "severity": ["info"],
                "output": "data/test_output.jsonl",
            }
        },
    }

    result = nuclei_helpers.get_profile(profiles, "no_profile", allow_null=True)
    assert result is None, "None value not returned when allow_null is True."


def test_get_profile_invalid_profiles():
    """Test passing a non-dictionary profiles argument."""
    profiles = ["not", "a", "dict"]
    with pytest.raises(TypeError, match="Expected a dictionary as 'data'."):
        nuclei_helpers.get_profile(profiles, "test_profile")


"""tests for build_nuclei_cmd"""


def test_build_nuclei_cmd_valid_profile(tmp_path):
    """build a command using all supported profile options."""

    output_file = tmp_path / "reports" / "results.json"
    profile = {
        "tags": ["web", "default"],
        "severity": ["medium", "high"],
        "rate_limit": 10,
        "concurrency": 5,
        "retries": 4,
        "timeout": 30,
        "output": str(output_file),
        "input_mode": "list",
    }

    targets = str(tmp_path / "targets.txt")

    with patch("tools.nuclei_helpers.os.makedirs") as mock_makedirs:
        cmd = nuclei_helpers.build_nuclei_cmd(profile, targets)

    mock_makedirs.assert_called_once_with(str(output_file.parent), exist_ok=True)

    assert cmd == [
        "nuclei",
        "-l",
        targets,
        "-im",
        "list",
        "-tags",
        "web,default",
        "-s",
        "medium,high",
        "-rl",
        "10",
        "-c",
        "5",
        "-retries",
        "4",
        "-timeout",
        "30",
        "-omit-raw",
        "-jle",
        str(output_file),
    ]


def test_build_nuclei_cmd_invalid_profile_type():
    """passing a non-dict profile should raise a TypeError."""

    with pytest.raises(TypeError, match="Expected a dictionary as 'profile'"):
        nuclei_helpers.build_nuclei_cmd([], "targets.txt")


def test_build_nuclei_cmd_missing_targets():
    """an empty or whitespace target string should raise a ValueError."""

    with pytest.raises(ValueError, match="A valid target must be provided"):
        nuclei_helpers.build_nuclei_cmd({}, "   ")


"""test run_nuclei function"""


def test_run_nuclei():
    """should delegate to subprocess.run with stderr piped and text enabled."""

    cmd = ["nuclei", "-version"]
    sentinel_result = subprocess.CompletedProcess(cmd, 0)

    with patch("tools.nuclei_helpers.subprocess.run") as mock_run_nuclei:
        mock_run_nuclei.return_value = sentinel_result

        result = nuclei_helpers.run_nuclei(cmd, timeout=15)

        mock_run_nuclei.assert_called_once_with(
            cmd,
            check=True,
            timeout=15,
            stderr=subprocess.PIPE,
            text=True,
        )

        assert result is sentinel_result
