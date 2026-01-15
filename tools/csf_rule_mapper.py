"""
CSF Rule-Based Mapper for Nuclei Findings

This module implements deterministic mapping of Nuclei findings to NIST CSF v2.0
subcategories using rule-based logic from mapping_rules.yaml.

Key features:
- Tag-based and severity-based rule matching
- Template-specific overrides
- Confidence scoring and rationale tracking
- CSF Function enrichment (Identify/Protect/Detect/Respond/Recover)
- Support for template cache enrichment
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import yaml


class CSFRuleMapper:
    """Maps Nuclei findings to NIST CSF subcategories using rules and overrides."""

    def __init__(
        self,
        mapping_rules_path: str,
        csf_lookup_path: str,
        template_cache_path: Optional[str] = None,
    ):
        """
        Initialize the CSF Rule Mapper.

        Args:
            mapping_rules_path: Path to mapping_rules.yaml
            csf_lookup_path: Path to csf_lookup.csv (for CSF function enrichment)
            template_cache_path: Optional path to template cache for tag enrichment
        """
        self.mapping_rules_path = Path(mapping_rules_path)
        self.csf_lookup_path = Path(csf_lookup_path)
        self.template_cache_path = Path(template_cache_path) if template_cache_path else None

        # Load configuration
        self.rules = []
        self.overrides = {}
        self.defaults = {}
        self.csf_function_map = {}
        self.template_cache = {}

        self._load_mapping_rules()
        self._load_csf_lookup()
        if self.template_cache_path:
            self._load_template_cache()

    def _load_mapping_rules(self):
        """Load and parse mapping_rules.yaml."""
        if not self.mapping_rules_path.exists():
            raise FileNotFoundError(f"Mapping rules not found: {self.mapping_rules_path}")

        with open(self.mapping_rules_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.defaults = data.get("defaults", {})
        self.rules = data.get("rules", [])

        # Build overrides lookup
        for override in data.get("overrides", []):
            template_id = override.get("template_id")
            if template_id:
                self.overrides[template_id] = {
                    "csf_subcats": override.get("csf_subcats", []),
                    "confidence": override.get("confidence", self.defaults.get("confidence", "Medium")),
                    "rationale": override.get("rationale", ""),
                }

    def _load_csf_lookup(self):
        """Load CSF lookup to map subcategory IDs to functions."""
        if not self.csf_lookup_path.exists():
            raise FileNotFoundError(f"CSF lookup not found: {self.csf_lookup_path}")

        df = pd.read_csv(self.csf_lookup_path)

        # Build mapping from subcategory_id to CSF function
        for _, row in df.iterrows():
            subcat_id = str(row.get("csf_subcategory_id", "")).strip()
            if subcat_id:
                # Extract function from subcategory ID (e.g., "ID.AM-02" -> "Identify")
                function = self._extract_csf_function(subcat_id)
                self.csf_function_map[subcat_id] = {
                    "function": function,
                    "name": row.get("csf_name", ""),
                    "weight": row.get("weight", 1.0),
                    "recommendation": row.get("recommendation", ""),
                }

    def _load_template_cache(self):
        """Load optional template cache for tag enrichment."""
        if not self.template_cache_path or not self.template_cache_path.exists():
            return

        try:
            with open(self.template_cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # Build lookup: template_id -> {tags: [], severity: ""}
            if isinstance(cache_data, dict):
                self.template_cache = cache_data
            elif isinstance(cache_data, list):
                # If it's a list of templates
                for template in cache_data:
                    template_id = template.get("id") or template.get("template_id")
                    if template_id:
                        self.template_cache[template_id] = {
                            "tags": template.get("tags", []),
                            "severity": template.get("severity", ""),
                        }
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not load template cache: {e}")

    @staticmethod
    def _extract_csf_function(subcategory_id: str) -> str:
        """
        Extract CSF Function from subcategory ID.

        Args:
            subcategory_id: CSF subcategory ID (e.g., "PR.AA-01")

        Returns:
            Full function name (e.g., "Protect")
        """
        prefix = subcategory_id.split(".")[0].upper() if "." in subcategory_id else ""

        function_map = {
            "GV": "Govern",
            "ID": "Identify",
            "PR": "Protect",
            "DE": "Detect",
            "RS": "Respond",
            "RC": "Recover",
        }

        return function_map.get(prefix, "Unknown")

    @staticmethod
    def _normalize_severity(severity: str) -> str:
        """Normalize severity to lowercase for comparison."""
        if not severity:
            return "info"
        return str(severity).strip().lower()

    @staticmethod
    def _severity_meets_min(finding_severity: str, min_severity: str) -> bool:
        """
        Check if finding severity meets minimum requirement.

        Args:
            finding_severity: Severity of the finding
            min_severity: Minimum required severity

        Returns:
            True if finding severity >= min_severity
        """
        severity_levels = {
            "info": 0,
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }

        finding_level = severity_levels.get(finding_severity, 0)
        min_level = severity_levels.get(min_severity, 0)

        return finding_level >= min_level

    def _enrich_finding_tags(self, finding: Dict[str, Any]) -> List[str]:
        """
        Enrich finding with tags from template cache if missing.

        Args:
            finding: Finding dictionary

        Returns:
            List of tags
        """
        tags = finding.get("tags", [])

        # If tags are missing and we have a template cache, look them up
        if not tags and self.template_cache:
            template_id = finding.get("templateID") or finding.get("template-id")
            if template_id and template_id in self.template_cache:
                cached = self.template_cache[template_id]
                tags = cached.get("tags", [])

        return tags if isinstance(tags, list) else []

    def _matches_rule_condition(self, finding: Dict[str, Any], when: Dict[str, Any]) -> bool:
        """
        Check if a finding matches a rule's conditions.

        Args:
            finding: Finding dictionary with templateID, severity, tags
            when: Rule condition from mapping_rules.yaml

        Returns:
            True if all conditions match
        """
        # Get finding attributes
        tags = self._enrich_finding_tags(finding)
        severity = self._normalize_severity(finding.get("severity", "info"))

        # Check any_tag condition
        any_tag = when.get("any_tag", [])
        if any_tag:
            # At least one tag must match
            if not any(tag in tags for tag in any_tag):
                return False

        # Check all_tag condition
        all_tag = when.get("all_tag", [])
        if all_tag:
            # All tags must be present
            if not all(tag in tags for tag in all_tag):
                return False

        # Check min_severity condition
        min_severity = when.get("min_severity")
        if min_severity:
            min_sev_normalized = self._normalize_severity(min_severity)
            if not self._severity_meets_min(severity, min_sev_normalized):
                return False

        return True

    def _apply_override(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Check for template-specific override.

        Args:
            template_id: Nuclei template ID

        Returns:
            Override mapping dict if found, None otherwise
        """
        return self.overrides.get(template_id)

    def _apply_rules(self, finding: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Apply mapping rules to a finding.

        Args:
            finding: Finding dictionary

        Returns:
            List of mapping results
        """
        results = []

        for rule in self.rules:
            when = rule.get("when", {})
            if self._matches_rule_condition(finding, when):
                map_config = rule.get("map", {})

                # Extract mapping configuration
                csf_subcats = map_config.get("csf_subcats", [])
                confidence = map_config.get("confidence", self.defaults.get("confidence", "Medium"))
                rationale = map_config.get("rationale", "")

                # Add rule name to rationale if present
                rule_name = rule.get("name", "")
                if rule_name:
                    rationale = f"{rule_name}: {rationale}" if rationale else rule_name

                for subcat_id in csf_subcats:
                    results.append(
                        {
                            "subcat_id": subcat_id,
                            "confidence": confidence,
                            "rationale": rationale,
                            "source": "rule",
                        }
                    )

        return results

    def map_finding(self, finding: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Map a single finding to CSF subcategories.

        Args:
            finding: Finding dictionary with at minimum: templateID, severity
                    Optional: tags, host, timestamp, matcher-name, description

        Returns:
            List of mapped results, each containing:
            {
                "timestamp": str,
                "host": str,
                "templateID": str,
                "severity": str,
                "matcher_name": str,
                "description": str,
                "subcat_id": str,
                "confidence": str,
                "rationale": str,
                "csf_function": str,
                "csf_subcategory_name": str,
                "weight": float,
                "recommendation": str
            }
        """
        template_id = finding.get("templateID") or finding.get("template-id", "")

        # Check for override first
        override = self._apply_override(template_id)
        if override:
            mappings = [
                {
                    "subcat_id": subcat_id,
                    "confidence": override.get("confidence", "Medium"),
                    "rationale": override.get("rationale", ""),
                    "source": "override",
                }
                for subcat_id in override.get("csf_subcats", [])
            ]
        else:
            # Apply rules
            mappings = self._apply_rules(finding)

        # If no mappings found, return empty
        if not mappings:
            return []

        # Enrich each mapping with CSF metadata
        results = []
        for mapping in mappings:
            subcat_id = mapping["subcat_id"]
            csf_meta = self.csf_function_map.get(subcat_id, {})

            result = {
                # Original finding fields
                "timestamp": finding.get("timestamp", ""),
                "host": finding.get("host", ""),
                "templateID": template_id,
                "severity": finding.get("severity", ""),
                "matcher_name": finding.get("matcher-name") or finding.get("matcher_name", ""),
                "description": finding.get("description", ""),
                # Mapping fields
                "subcat_id": subcat_id,
                "confidence": mapping["confidence"],
                "rationale": mapping["rationale"],
                # CSF enrichment
                "csf_function": csf_meta.get("function", "Unknown"),
                "csf_subcategory_name": csf_meta.get("name", ""),
                "weight": csf_meta.get("weight", 1.0),
                "recommendation": csf_meta.get("recommendation", ""),
            }

            results.append(result)

        return results

    def map_findings(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Map multiple findings to CSF subcategories.

        Args:
            findings: List of finding dictionaries

        Returns:
            List of all mapped results (flattened)
        """
        all_results = []

        for finding in findings:
            mapped = self.map_finding(finding)
            all_results.extend(mapped)

        return all_results


def write_jsonl(data: List[Dict[str, Any]], output_path: str):
    """
    Write data to JSONL format (newline-delimited JSON).

    Args:
        data: List of dictionaries to write
        output_path: Path to output file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for record in data:
            f.write(json.dumps(record) + "\n")


def write_csv(data: List[Dict[str, Any]], output_path: str):
    """
    Write data to CSV format.

    Args:
        data: List of dictionaries to write
        output_path: Path to output file
    """
    if not data:
        print("Warning: No data to write to CSV")
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)


__all__ = [
    "CSFRuleMapper",
    "write_jsonl",
    "write_csv",
]
