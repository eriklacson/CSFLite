"""Tests for the Nuclei raw JSON converter utilities."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

# Ensure the project root is available *before* any site-packages "tools" module.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.nuclei_json_converter import (  # noqa: E402
    convert_nuclei_raw,
    convert_nuclei_raw_file,
)


@pytest.fixture(scope="module")
def nuclei_baseline_entry() -> Dict[str, Any]:
    """Load the baseline scan once so multiple tests can reuse it."""

    sample_path = Path("scans/nuclei_baseline_web.json")
    return json.loads(sample_path.read_text(encoding="utf-8"))


@pytest.fixture
def sample_entry() -> Dict[str, Any]:
    """Return a minimal mutable raw entry for parametrised tests."""

    return {
        "template-id": "example",
        "info": {
            "name": "Example Template",
            "description": "Example description.",
            "severity": "low",
        },
        "host": "https://example.com",
        "matched-at": "https://example.com/path",
        "timestamp": "2025-01-01T00:00:00Z",
    }


def test_convert_nuclei_raw_file_single_entry(tmp_path: Path, nuclei_baseline_entry: Dict[str, Any]):
    """A single JSON object should produce a list with one normalized entry."""

    # Write to a temporary file to exercise the file-loading code path.
    temp_file = tmp_path / "baseline.json"
    temp_file.write_text(json.dumps(nuclei_baseline_entry), encoding="utf-8")

    results = convert_nuclei_raw_file(temp_file)
    assert isinstance(results, list)
    assert len(results) == 1

    entry = results[0]
    assert entry["templateID"] == "prometheus-metrics"
    assert entry["host"] == "juice-shop.herokuapp.com"
    assert entry["matched-at"] == "https://juice-shop.herokuapp.com/metrics"
    assert entry["severity"] == "medium"
    assert entry["timestamp"] == "2025-10-11T15:58:30.076533302+08:00"
    assert entry["matcher-name"] == "Prometheus Metrics - Detect"
    assert entry["description"].startswith("Prometheus metrics page was detected")


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("matcher-name", "custom-matcher"),
        ("matcher-name", ""),
    ],
)
def test_convert_nuclei_raw_handles_optional_fields(field: str, expected: str, sample_entry: Dict[str, Any]) -> None:
    """Optional fields should default to sensible values when missing."""

    if expected:
        sample_entry[field] = expected

    results = convert_nuclei_raw(sample_entry)
    assert len(results) == 1

    entry = results[0]
    assert entry["templateID"] == "example"
    assert entry["matcher-name"] == (expected or "Example Template")
    assert entry["description"] == "Example description."
    assert entry["severity"] == "low"


def test_convert_nuclei_raw_accepts_sequence() -> None:
    """Sequences of entries should be normalised into multiple results."""

    raw_entries = [
        {
            "template-id": "first",
            "info": {"name": "First", "severity": "high"},
            "host": "https://first.example",
            "matched-at": "https://first.example/path",
        },
        {
            "templateID": "second",
            "info": {"name": "Second", "severity": "low"},
            "url": "https://second.example",
        },
    ]

    results = convert_nuclei_raw(raw_entries)
    assert [entry["templateID"] for entry in results] == ["first", "second"]
    assert results[0]["host"] == "https://first.example"
    assert results[1]["host"] == "https://second.example"


@pytest.mark.parametrize(
    ("raw_data", "error_message"),
    [
        (42, "Raw Nuclei data must"),
        ([{"template-id": "ok"}, "not-a-mapping"], "Each entry in the raw Nuclei data must"),
    ],
)
def test_convert_nuclei_raw_invalid_inputs(raw_data, error_message) -> None:
    """Invalid shapes should surface the coercion errors."""

    with pytest.raises(TypeError, match=error_message):
        convert_nuclei_raw(raw_data)  # type: ignore[arg-type]
