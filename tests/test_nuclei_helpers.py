# Unit test for nuclei_helpers.py

# Standard Library Modules
import os
import sys
from textwrap import dedent
from unittest.mock import mock_open, patch

import pytest  # noqa: F401

# Third-Party Modules
import yaml

# Local Helper Module
import tools.nuclei_helpers as nuclei_helpers

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


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
