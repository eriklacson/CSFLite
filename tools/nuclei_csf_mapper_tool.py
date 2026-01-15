#!/usr/bin/env python3
"""
Nuclei to CSF Mapper Tool

Command-line tool to transform Nuclei findings into deterministic mappings
to NIST CSF v2.0 subcategories, enriched with CSF Functions.

Usage:
    python nuclei_csf_mapper_tool.py \\
        --input scans/nuclei_converted.json \\
        --output-csv output/csf_mapped.csv \\
        --output-jsonl output/csf_mapped.jsonl \\
        --mapping-rules data/mapping_rules.yaml \\
        --csf-lookup data/csf_lookup.csv
"""

import argparse
import json
import sys
from pathlib import Path

from csf_rule_mapper import CSFRuleMapper, write_csv, write_jsonl


def load_findings(input_path: str) -> list:
    """
    Load findings from JSON or JSONL file.

    Args:
        input_path: Path to input file

    Returns:
        List of finding dictionaries
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    findings = []

    # Try JSON first
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                findings = data
            elif isinstance(data, dict):
                findings = [data]
            else:
                raise ValueError("Input JSON must be a list or dict")

    except json.JSONDecodeError:
        # Try JSONL
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    findings.append(json.loads(line))

    return findings


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Map Nuclei findings to NIST CSF v2.0 subcategories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Input/Output
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Input file with converted Nuclei findings (JSON or JSONL)",
    )
    parser.add_argument(
        "--output-csv",
        help="Output CSV file path",
    )
    parser.add_argument(
        "--output-jsonl",
        help="Output JSONL file path",
    )
    parser.add_argument(
        "--output-json",
        help="Output JSON file path",
    )

    # Configuration
    parser.add_argument(
        "--mapping-rules",
        default="data/mapping_rules.yaml",
        help="Path to mapping_rules.yaml (default: data/mapping_rules.yaml)",
    )
    parser.add_argument(
        "--csf-lookup",
        default="data/csf_lookup.csv",
        help="Path to csf_lookup.csv (default: data/csf_lookup.csv)",
    )
    parser.add_argument(
        "--template-cache",
        help="Optional path to template cache for tag enrichment",
    )

    # Options
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    # Validate that at least one output is specified
    if not (args.output_csv or args.output_jsonl or args.output_json):
        parser.error("At least one output format must be specified (--output-csv, --output-jsonl, or --output-json)")

    try:
        # Load findings
        if args.verbose:
            print(f"Loading findings from: {args.input}")

        findings = load_findings(args.input)

        if args.verbose:
            print(f"Loaded {len(findings)} findings")

        # Initialize mapper
        if args.verbose:
            print("Initializing CSF Rule Mapper")
            print(f"  Mapping rules: {args.mapping_rules}")
            print(f"  CSF lookup: {args.csf_lookup}")
            if args.template_cache:
                print(f"  Template cache: {args.template_cache}")

        mapper = CSFRuleMapper(
            mapping_rules_path=args.mapping_rules,
            csf_lookup_path=args.csf_lookup,
            template_cache_path=args.template_cache,
        )

        # Map findings
        if args.verbose:
            print("Mapping findings to CSF subcategories...")

        mapped_results = mapper.map_findings(findings)

        if args.verbose:
            print(f"Generated {len(mapped_results)} mapped records")

        # Write outputs
        if args.output_csv:
            if args.verbose:
                print(f"Writing CSV output to: {args.output_csv}")
            write_csv(mapped_results, args.output_csv)

        if args.output_jsonl:
            if args.verbose:
                print(f"Writing JSONL output to: {args.output_jsonl}")
            write_jsonl(mapped_results, args.output_jsonl)

        if args.output_json:
            if args.verbose:
                print(f"Writing JSON output to: {args.output_json}")
            output_path = Path(args.output_json)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(mapped_results, f, indent=2)

        if args.verbose:
            print("✓ Mapping completed successfully")

        # Print summary statistics
        if args.verbose:
            csf_functions = {}
            confidence_levels = {}

            for record in mapped_results:
                func = record.get("csf_function", "Unknown")
                conf = record.get("confidence", "Unknown")

                csf_functions[func] = csf_functions.get(func, 0) + 1
                confidence_levels[conf] = confidence_levels.get(conf, 0) + 1

            print("\nSummary:")
            print(f"  Total findings: {len(findings)}")
            print(f"  Total mapped records: {len(mapped_results)}")
            print(f"  Unique template IDs: {len(set(f.get('templateID', '') for f in findings))}")
            print("  CSF Functions:")
            for func, count in sorted(csf_functions.items()):
                print(f"    {func}: {count}")
            print("  Confidence levels:")
            for conf, count in sorted(confidence_levels.items()):
                print(f"    {conf}: {count}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
