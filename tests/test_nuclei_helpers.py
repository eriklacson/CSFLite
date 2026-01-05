# Unit test for nuclei_helpers.py

# Standard Library Modules
import io
import subprocess
from pathlib import Path
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

    output_file = tmp_path / "output" / "results.json"
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

    targets_path = tmp_path / "targets.txt"
    targets_path.touch()
    targets = str(targets_path)

    with patch("tools.nuclei_helpers.os.makedirs") as mock_makedirs:
        cmd = nuclei_helpers.build_nuclei_cmd(profile, targets)

    mock_makedirs.assert_called_once_with(output_file.parent, exist_ok=True)

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
        "-je",
        str(output_file.resolve()),
    ]


def test_build_nuclei_cmd_scan_directory_override(tmp_path):
    """overriding the scan directory should relocate the output file while keeping the filename."""

    profile = {"output": "scans/custom_scan.jsonl"}
    targets_path = tmp_path / "targets.txt"
    targets_path.touch()

    custom_dir = tmp_path / "custom-output"

    with patch("tools.nuclei_helpers.os.makedirs") as mock_makedirs:
        cmd = nuclei_helpers.build_nuclei_cmd(
            profile,
            str(targets_path),
            scan_directory=str(custom_dir),
        )

    mock_makedirs.assert_called_once_with(custom_dir.resolve(), exist_ok=True)

    expected_output = custom_dir / "custom_scan.jsonl"
    assert cmd[-2:] == ["-je", str(expected_output.resolve())]


def test_build_nuclei_cmd_invalid_profile_type():
    """passing a non-dict profile should raise a TypeError."""

    with pytest.raises(TypeError, match="Expected a dictionary as 'profile'"):
        nuclei_helpers.build_nuclei_cmd([], "targets.txt")


def test_build_nuclei_cmd_missing_targets():
    """an empty or whitespace target string should raise a ValueError."""

    with pytest.raises(ValueError, match="A valid target must be provided"):
        nuclei_helpers.build_nuclei_cmd({}, "   ")


def test_build_nuclei_cmd_missing_targets_file(monkeypatch, tmp_path):
    """a missing targets file should raise a FileNotFoundError."""

    monkeypatch.chdir(tmp_path)

    with patch("tools.nuclei_helpers.os.makedirs"):
        with pytest.raises(FileNotFoundError, match="Targets file 'missing.txt'"):
            nuclei_helpers.build_nuclei_cmd({}, "missing.txt")


def test_build_nuclei_cmd_resolves_relative_targets(monkeypatch):
    """relative targets should resolve against the project root when needed."""

    project_root = Path(__file__).resolve().parent.parent
    targets_file = project_root / "data" / "targets.txt"

    # simulate running the helper from the tools directory where the relative path would fail
    monkeypatch.chdir(project_root / "tools")

    with patch("tools.nuclei_helpers.os.makedirs"):
        cmd = nuclei_helpers.build_nuclei_cmd({}, "data/targets.txt")

    assert cmd[1:3] == ["-l", str(targets_file.resolve())]


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


def test_run_nuclei_accepts_command_string():
    """string commands should be split and passed to subprocess.run."""

    cmd = "nuclei -version"
    sentinel_result = subprocess.CompletedProcess(["nuclei", "-version"], 0)

    with patch("tools.nuclei_helpers.subprocess.run") as mock_run_nuclei:
        mock_run_nuclei.return_value = sentinel_result
        result = nuclei_helpers.run_nuclei(cmd)

    mock_run_nuclei.assert_called_once_with(
        ["nuclei", "-version"],
        check=True,
        timeout=None,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result is sentinel_result


def test_run_nuclei_rejects_invalid_command_type():
    """non-iterables or non-strings should raise a TypeError."""

    with pytest.raises(TypeError, match="Command must be a string"):
        nuclei_helpers.run_nuclei(123)  # type: ignore[arg-type]


def test_run_nuclei_rejects_non_string_arguments():
    """iterables containing non-string args should raise a TypeError."""

    with pytest.raises(TypeError, match="Command arguments must be strings"):
        nuclei_helpers.run_nuclei(["nuclei", 1])  # type: ignore[list-item]


def test_run_nuclei_surfaces_stderr_output():
    """stderr emitted by nuclei should be forwarded to sys.stderr."""

    cmd = ["nuclei", "-version"]
    completed = subprocess.CompletedProcess(cmd, 0, stderr="warning")

    with (
        patch("tools.nuclei_helpers.subprocess.run", return_value=completed),
        patch("sys.stderr", new_callable=io.StringIO) as fake_stderr,
    ):
        nuclei_helpers.run_nuclei(cmd)

    assert fake_stderr.getvalue() == "warning\n"


def test_run_nuclei_surfaces_stderr_on_error():
    """stderr emitted when nuclei fails should be written before re-raising."""

    cmd = ["nuclei", "-version"]
    error = subprocess.CalledProcessError(1, cmd, stderr="boom")

    with (
        patch("tools.nuclei_helpers.subprocess.run", side_effect=error),
        patch("sys.stderr", new_callable=io.StringIO) as fake_stderr,
    ):
        with pytest.raises(subprocess.CalledProcessError):
            nuclei_helpers.run_nuclei(cmd)

    assert fake_stderr.getvalue() == "boom\n"


def test_run_nuclei_reports_missing_binary():
    """missing nuclei executable should raise a helpful runtime error."""

    cmd = ["nuclei", "-version"]

    with (
        patch("tools.nuclei_helpers.subprocess.run", side_effect=FileNotFoundError),
        pytest.raises(RuntimeError, match="Failed to execute nuclei command") as excinfo,
    ):
        nuclei_helpers.run_nuclei(cmd)

    assert "Ensure nuclei is installed" in str(excinfo.value)
