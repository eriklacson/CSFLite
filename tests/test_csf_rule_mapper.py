"""
Tests for CSF Rule Mapper

Tests the rule-based mapping of Nuclei findings to NIST CSF v2.0 subcategories.
"""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from tools.csf_rule_mapper import CSFRuleMapper, write_csv, write_jsonl


@pytest.fixture
def sample_mapping_rules():
    """Create a sample mapping_rules.yaml for testing."""
    rules = {
        "version": 1,
        "defaults": {
            "confidence": "Medium",
            "rationale_prefix": "rule:",
        },
        "rules": [
            {
                "name": "Transport security (TLS/HSTS/Headers)",
                "when": {"any_tag": ["ssl", "tls", "hsts", "headers"], "min_severity": "medium"},
                "map": {
                    "csf_subcats": ["PR.IR-01"],
                    "confidence": "High",
                    "rationale": "TLS config + secure transport signals",
                },
            },
            {
                "name": "Exposed backups & secrets",
                "when": {"any_tag": ["backup", "exposure", "secret", "s3", "cloud", "git", "env", "token"]},
                "map": {
                    "csf_subcats": ["PR.DS-01"],
                    "confidence": "High",
                    "rationale": "At-rest/backup exposure indicates inventory & protection gaps",
                },
            },
            {
                "name": "Fingerprinting & service discovery",
                "when": {"any_tag": ["tech", "cloud", "network", "discovery", "port"], "min_severity": "info"},
                "map": {
                    "csf_subcats": ["ID.AM-02", "ID.AM-03"],
                    "confidence": "Medium",
                    "rationale": "External discovery informs inventory and flows",
                },
            },
        ],
        "overrides": [
            {
                "template_id": "networking/open-ports",
                "csf_subcats": ["ID.AM-02", "ID.AM-03", "DE.CM-01"],
                "confidence": "Medium",
                "rationale": "Open ports discovery evidences inventory/flows",
            }
        ],
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(rules, f)
        return f.name


@pytest.fixture
def sample_csf_lookup():
    """Create a sample csf_lookup.csv for testing."""
    lookup_data = (
        "csf_subcategory_id,csf_name,weight,recommendation\n"
        "ID.AM-02,Assets and systems are inventoried,1.2,Maintain an up-to-date asset inventory\n"
        "ID.AM-03,Baseline of operations/data flows established,1.2,Establish and maintain baseline\n"
        "PR.DS-01,Data-at-rest is protected,1.0,Use full-disk encryption\n"
        "PR.IR-01,Communications and control networks are protected,1.2,Disable insecure protocols\n"
        "DE.CM-01,The network is monitored to detect events,1.2,Implement network monitoring\n"
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(lookup_data)
        return f.name


@pytest.fixture
def sample_template_cache():
    """Create a sample template cache for testing."""
    cache = {
        "tls-version": {"tags": ["ssl", "tls"], "severity": "info"},
        "http-missing-security-headers": {"tags": ["misconfig", "headers", "generic"], "severity": "info"},
        "networking/open-ports": {"tags": ["network", "port"], "severity": "info"},
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(cache, f)
        return f.name


def test_rule_mapper_initialization(sample_mapping_rules, sample_csf_lookup):
    """Test that the mapper initializes correctly."""
    mapper = CSFRuleMapper(
        mapping_rules_path=sample_mapping_rules,
        csf_lookup_path=sample_csf_lookup,
    )

    assert len(mapper.rules) == 3
    assert len(mapper.overrides) == 1
    assert "networking/open-ports" in mapper.overrides
    assert mapper.defaults["confidence"] == "Medium"


def test_extract_csf_function():
    """Test CSF function extraction from subcategory IDs."""
    assert CSFRuleMapper._extract_csf_function("ID.AM-02") == "Identify"
    assert CSFRuleMapper._extract_csf_function("PR.DS-01") == "Protect"
    assert CSFRuleMapper._extract_csf_function("DE.CM-01") == "Detect"
    assert CSFRuleMapper._extract_csf_function("RS.MA-01") == "Respond"
    assert CSFRuleMapper._extract_csf_function("RC.RP-01") == "Recover"
    assert CSFRuleMapper._extract_csf_function("GV.P0-01") == "Govern"
    assert CSFRuleMapper._extract_csf_function("INVALID") == "Unknown"


def test_severity_comparison():
    """Test severity level comparison."""
    assert CSFRuleMapper._severity_meets_min("high", "medium") is True
    assert CSFRuleMapper._severity_meets_min("medium", "medium") is True
    assert CSFRuleMapper._severity_meets_min("low", "medium") is False
    assert CSFRuleMapper._severity_meets_min("critical", "high") is True
    assert CSFRuleMapper._severity_meets_min("info", "low") is False


def test_rule_matching_with_tags(sample_mapping_rules, sample_csf_lookup):
    """Test that rules match correctly based on tags."""
    mapper = CSFRuleMapper(
        mapping_rules_path=sample_mapping_rules,
        csf_lookup_path=sample_csf_lookup,
    )

    # Finding with TLS tags should match transport security rule
    finding = {
        "templateID": "tls-version",
        "host": "example.com",
        "severity": "medium",
        "tags": ["ssl", "tls"],
        "timestamp": "2025-01-01T00:00:00Z",
        "matcher-name": "TLS Version",
        "description": "TLS version detection",
    }

    results = mapper.map_finding(finding)

    assert len(results) > 0
    assert any(r["subcat_id"] == "PR.IR-01" for r in results)
    assert any(r["confidence"] == "High" for r in results)
    assert any(r["csf_function"] == "Protect" for r in results)


def test_rule_matching_with_severity(sample_mapping_rules, sample_csf_lookup):
    """Test that rules respect minimum severity requirements."""
    mapper = CSFRuleMapper(
        mapping_rules_path=sample_mapping_rules,
        csf_lookup_path=sample_csf_lookup,
    )

    # Finding with TLS tags but low severity should NOT match (requires medium+)
    finding = {
        "templateID": "tls-info",
        "host": "example.com",
        "severity": "info",
        "tags": ["ssl", "tls"],
        "timestamp": "2025-01-01T00:00:00Z",
    }

    results = mapper.map_finding(finding)

    # Should not match the transport security rule (requires medium+)
    # but might match other rules that accept info severity
    assert not any(r["subcat_id"] == "PR.IR-01" for r in results)


def test_override_takes_precedence(sample_mapping_rules, sample_csf_lookup):
    """Test that template-specific overrides take precedence over rules."""
    mapper = CSFRuleMapper(
        mapping_rules_path=sample_mapping_rules,
        csf_lookup_path=sample_csf_lookup,
    )

    finding = {
        "templateID": "networking/open-ports",
        "host": "example.com",
        "severity": "info",
        "tags": ["network", "port"],
        "timestamp": "2025-01-01T00:00:00Z",
    }

    results = mapper.map_finding(finding)

    # Should use override, not rules
    assert len(results) == 3  # Override specifies 3 subcategories
    subcats = [r["subcat_id"] for r in results]
    assert "ID.AM-02" in subcats
    assert "ID.AM-03" in subcats
    assert "DE.CM-01" in subcats


def test_template_cache_enrichment(sample_mapping_rules, sample_csf_lookup, sample_template_cache):
    """Test that template cache enriches findings with missing tags."""
    mapper = CSFRuleMapper(
        mapping_rules_path=sample_mapping_rules,
        csf_lookup_path=sample_csf_lookup,
        template_cache_path=sample_template_cache,
    )

    # Finding WITHOUT tags - should get enriched from cache
    finding = {
        "templateID": "tls-version",
        "host": "example.com",
        "severity": "medium",
        "timestamp": "2025-01-01T00:00:00Z",
    }

    results = mapper.map_finding(finding)

    # Should match transport security rule because tags were enriched
    assert len(results) > 0
    assert any(r["subcat_id"] == "PR.IR-01" for r in results)


def test_multiple_findings_mapping(sample_mapping_rules, sample_csf_lookup):
    """Test mapping multiple findings at once."""
    mapper = CSFRuleMapper(
        mapping_rules_path=sample_mapping_rules,
        csf_lookup_path=sample_csf_lookup,
    )

    findings = [
        {
            "templateID": "tls-version",
            "host": "example.com",
            "severity": "medium",
            "tags": ["ssl", "tls"],
            "timestamp": "2025-01-01T00:00:00Z",
        },
        {
            "templateID": "exposed-secret",
            "host": "example.com",
            "severity": "high",
            "tags": ["secret", "exposure"],
            "timestamp": "2025-01-01T00:00:00Z",
        },
    ]

    results = mapper.map_findings(findings)

    assert len(results) > 0
    # Should have mappings from both findings
    template_ids = set(r["templateID"] for r in results)
    assert "tls-version" in template_ids
    assert "exposed-secret" in template_ids


def test_csf_function_enrichment(sample_mapping_rules, sample_csf_lookup):
    """Test that CSF functions are correctly enriched in results."""
    mapper = CSFRuleMapper(
        mapping_rules_path=sample_mapping_rules,
        csf_lookup_path=sample_csf_lookup,
    )

    finding = {
        "templateID": "test",
        "host": "example.com",
        "severity": "info",
        "tags": ["network", "port"],
        "timestamp": "2025-01-01T00:00:00Z",
    }

    results = mapper.map_finding(finding)

    # Check that all results have CSF metadata
    for result in results:
        assert "csf_function" in result
        assert result["csf_function"] in ["Identify", "Protect", "Detect", "Respond", "Recover", "Govern"]
        assert "csf_subcategory_name" in result
        assert "weight" in result
        assert "recommendation" in result


def test_no_match_returns_empty(sample_mapping_rules, sample_csf_lookup):
    """Test that findings with no matching rules return empty list."""
    mapper = CSFRuleMapper(
        mapping_rules_path=sample_mapping_rules,
        csf_lookup_path=sample_csf_lookup,
    )

    finding = {
        "templateID": "unknown-template",
        "host": "example.com",
        "severity": "info",
        "tags": ["unmatched", "notfound"],
        "timestamp": "2025-01-01T00:00:00Z",
    }

    results = mapper.map_finding(finding)

    assert len(results) == 0


def test_write_jsonl():
    """Test JSONL output writing."""
    data = [
        {"id": 1, "name": "test1"},
        {"id": 2, "name": "test2"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        output_path = f.name

    write_jsonl(data, output_path)

    # Read back and verify
    with open(output_path, "r") as f:
        lines = f.readlines()

    assert len(lines) == 2
    assert json.loads(lines[0]) == {"id": 1, "name": "test1"}
    assert json.loads(lines[1]) == {"id": 2, "name": "test2"}

    Path(output_path).unlink()


def test_write_csv():
    """Test CSV output writing."""
    data = [
        {"id": 1, "name": "test1", "severity": "high"},
        {"id": 2, "name": "test2", "severity": "medium"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        output_path = f.name

    write_csv(data, output_path)

    # Read back and verify
    import pandas as pd

    df = pd.read_csv(output_path)

    assert len(df) == 2
    assert list(df.columns) == ["id", "name", "severity"]
    assert df.iloc[0]["name"] == "test1"

    Path(output_path).unlink()


def test_confidence_and_rationale_in_output(sample_mapping_rules, sample_csf_lookup):
    """Test that confidence and rationale are included in output."""
    mapper = CSFRuleMapper(
        mapping_rules_path=sample_mapping_rules,
        csf_lookup_path=sample_csf_lookup,
    )

    finding = {
        "templateID": "tls-version",
        "host": "example.com",
        "severity": "medium",
        "tags": ["ssl", "tls"],
        "timestamp": "2025-01-01T00:00:00Z",
    }

    results = mapper.map_finding(finding)

    assert len(results) > 0
    for result in results:
        assert "confidence" in result
        assert "rationale" in result
        assert result["confidence"] in ["Low", "Medium", "High"]
        assert isinstance(result["rationale"], str)


def test_all_finding_fields_preserved(sample_mapping_rules, sample_csf_lookup):
    """Test that all original finding fields are preserved in output."""
    mapper = CSFRuleMapper(
        mapping_rules_path=sample_mapping_rules,
        csf_lookup_path=sample_csf_lookup,
    )

    finding = {
        "templateID": "test-template",
        "host": "example.com",
        "severity": "high",
        "tags": ["secret"],
        "timestamp": "2025-01-01T12:00:00Z",
        "matcher-name": "Test Matcher",
        "description": "Test description",
    }

    results = mapper.map_finding(finding)

    assert len(results) > 0
    for result in results:
        assert result["templateID"] == "test-template"
        assert result["host"] == "example.com"
        assert result["severity"] == "high"
        assert result["timestamp"] == "2025-01-01T12:00:00Z"
        assert result["matcher_name"] == "Test Matcher"
        assert result["description"] == "Test description"
