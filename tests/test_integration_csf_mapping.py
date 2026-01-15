"""
Integration tests for Nuclei to CSF mapping

Tests the complete pipeline from raw Nuclei output to mapped CSF results.
"""

from pathlib import Path

from tools import nuclei_json_converter
from tools.csf_rule_mapper import CSFRuleMapper


def test_end_to_end_mapping():
    """Test complete pipeline: raw Nuclei -> converted -> mapped to CSF."""

    # Sample raw Nuclei finding
    raw_finding = {
        "template-id": "tls-version",
        "host": "example.com",
        "matched-at": "example.com:443",
        "timestamp": "2025-01-01T00:00:00Z",
        "info": {
            "name": "TLS Version - Detect",
            "severity": "medium",
            "tags": ["ssl", "tls"],
            "description": "TLS version detection",
        },
    }

    # Step 1: Convert raw Nuclei output
    converted = nuclei_json_converter.convert_nuclei_raw([raw_finding])

    assert len(converted) == 1
    assert converted[0]["templateID"] == "tls-version"
    assert converted[0]["tags"] == ["ssl", "tls"]
    assert converted[0]["severity"] == "medium"

    # Step 2: Map to CSF using rules
    mapper = CSFRuleMapper(
        mapping_rules_path="data/mapping_rules.yaml",
        csf_lookup_path="data/csf_lookup.csv",
    )

    mapped = mapper.map_findings(converted)

    # Should have at least one mapping
    assert len(mapped) > 0

    # Check that mappings contain required fields
    for record in mapped:
        assert "subcat_id" in record
        assert "csf_function" in record
        assert "confidence" in record
        assert "rationale" in record
        assert "csf_subcategory_name" in record
        assert record["csf_function"] in [
            "Identify",
            "Protect",
            "Detect",
            "Respond",
            "Recover",
            "Govern",
        ]

    # For TLS finding with medium severity, should map to PR.IR-01
    pr_ir_mappings = [r for r in mapped if r["subcat_id"] == "PR.IR-01"]
    assert len(pr_ir_mappings) > 0
    assert pr_ir_mappings[0]["csf_function"] == "Protect"
    assert pr_ir_mappings[0]["confidence"] == "High"


def test_override_precedence():
    """Test that template overrides take precedence over rules."""

    raw_finding = {
        "template-id": "networking/open-ports",
        "host": "example.com",
        "info": {
            "name": "Open Ports",
            "severity": "info",
            "tags": ["network", "port"],
        },
    }

    # Convert
    converted = nuclei_json_converter.convert_nuclei_raw([raw_finding])

    # Map
    mapper = CSFRuleMapper(
        mapping_rules_path="data/mapping_rules.yaml",
        csf_lookup_path="data/csf_lookup.csv",
    )

    mapped = mapper.map_findings(converted)

    # Should have 3 mappings from override (not from rules)
    assert len(mapped) == 3

    subcats = [r["subcat_id"] for r in mapped]
    assert "ID.AM-02" in subcats
    assert "ID.AM-03" in subcats
    assert "DE.CM-01" in subcats


def test_tags_preserved_in_conversion():
    """Test that tags are preserved during conversion."""

    raw_finding = {
        "template-id": "test-template",
        "host": "example.com",
        "info": {
            "name": "Test",
            "severity": "high",
            "tags": ["cve", "wordpress", "exposure"],
        },
    }

    converted = nuclei_json_converter.convert_nuclei_raw([raw_finding])

    assert len(converted) == 1
    assert "tags" in converted[0]
    assert converted[0]["tags"] == ["cve", "wordpress", "exposure"]


def test_csv_header_matches_output():
    """Test that CSV headers match the mapper output fields."""

    import tempfile

    import pandas as pd

    from tools.csf_rule_mapper import write_csv

    # Create sample mapped data
    mapped_data = [
        {
            "timestamp": "2025-01-01T00:00:00Z",
            "host": "example.com",
            "templateID": "test",
            "severity": "high",
            "matcher_name": "Test",
            "description": "Test description",
            "subcat_id": "PR.DS-01",
            "confidence": "High",
            "rationale": "Test rationale",
            "csf_function": "Protect",
            "csf_subcategory_name": "Data-at-rest is protected",
            "weight": 1.0,
            "recommendation": "Use encryption",
        }
    ]

    # Write to CSV
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        output_path = f.name

    write_csv(mapped_data, output_path)

    # Read back and verify
    df = pd.read_csv(output_path)

    expected_columns = [
        "timestamp",
        "host",
        "templateID",
        "severity",
        "matcher_name",
        "description",
        "subcat_id",
        "confidence",
        "rationale",
        "csf_function",
        "csf_subcategory_name",
        "weight",
        "recommendation",
    ]

    assert list(df.columns) == expected_columns
    assert len(df) == 1
    assert df.iloc[0]["csf_function"] == "Protect"

    # Cleanup
    Path(output_path).unlink()
