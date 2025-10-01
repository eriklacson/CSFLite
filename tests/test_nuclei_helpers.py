# Unit test for nuclei_helpers.py

import sys
import os

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import necessary modules
import yaml
import pytest  # noqa: F401
from unittest.mock import mock_open, patch

# Local Helper Module
import tools.nuclei_helpers as nuclei_helpers


def test_load_profile_valid():
    """Test the load_profile function with a mock YAML file."""

    # Mock YAML content
    mock_yaml_content = """
    version: 1
    profiles:
      test_profile:
        tags: [test, mock]
        severity: [info]
        output: data/test_output.jsonl
    """

    # Mock the open function and patch it in the context of the load_profiles function
    with patch("builtins.open", mock_open(read_data=mock_yaml_content)):
        # Call the function with a mock file path
        profiles = nuclei_helpers.load_profiles("mock_profiles.yaml")

        # Assertions
        assert profiles["version"] == 1
        assert "test_profile" in profiles["profiles"]
        assert profiles["profiles"]["test_profile"]["tags"] == ["test", "mock"]
        assert profiles["profiles"]["test_profile"]["output"] == "data/test_output.jsonl"
        assert profiles["profiles"]["test_profile"]["severity"] == ["info"]


def test_load_profile_file_not_found():
    """Test load_profiles function when the file does not exist."""
    with pytest.raises(FileNotFoundError):
        nuclei_helpers.load_profiles("non_existent_file.yaml")


def test_load_profile_invalid_yaml():
    """Test load_profiles function with invalid YAML content."""
    mock_invalid_yaml_content = """
    version: 1
    profiles:
      test_profile
        tags: [test, mock]
        severity: [info]
        output: data/test_output.jsonl
    """  # Missing colon after test_profile

    with patch("builtins.open", mock_open(read_data=mock_invalid_yaml_content)):
        with pytest.raises(
            yaml.YAMLError
        ):  # Replace Exception with the specific exception type if known
            nuclei_helpers.load_profiles("mock_invalid_profiles.yaml")


def test_get_profile_valid():
    """Test retrieving an existing profile."""
    profiles = {"test_profile": {"key": "value"}}
    result = nuclei_helpers.get_profile(profiles, "test_profile")
    assert result == {"key": "value"}


def test_get_profile_missing():
    """Test retrieving a non-existent profile with a default value."""
    profiles = {"test_profile": {"key": "value"}}
    result = nuclei_helpers.get_profile(profiles, "missing_profile", default="default_value")
    assert result == "default_value"


def test_get_profile_null_not_allowed():
    """Test retrieving a profile with None value when allow_null is False."""
    profiles = {"test_profile": None}
    result = nuclei_helpers.get_profile(
        profiles, "test_profile", default="default_value", allow_null=False
    )
    assert result == "default_value"


def test_get_profile_null_allowed():
    """Test retrieving a profile with None value when allow_null is True."""
    profiles = {"test_profile": None}
    result = nuclei_helpers.get_profile(
        profiles, "test_profile", default="default_value", allow_null=True
    )
    assert result is None


def test_get_profile_invalid_profiles():
    """Test passing a non-dictionary profiles argument."""
    profiles = ["not", "a", "dict"]
    with pytest.raises(TypeError, match="Expected a dictionary as 'data'."):
        nuclei_helpers.get_profile(profiles, "test_profile")
